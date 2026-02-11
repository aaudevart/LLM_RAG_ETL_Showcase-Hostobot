from agents.hospital_rag_agent import hospital_rag_agent
from fastapi import FastAPI
from models.hospital_rag_query import HospitalQueryInput, HospitalQueryOutput
from utils.async_utils import async_retry_generator
import json

app = FastAPI(
    title="Hospital Chatbot",
    description="Endpoints for a hospital system graph RAG chatbot",
)

@async_retry_generator(max_retries=3, delay=1)
async def stream_agent_with_retry(query: str):
    """
    Stream the agents events with a retry logic.
    """
    input_data = {"messages": [{"role": "human", "content": query}]}
    
    # Use astream to retrieve the events
    async for event in hospital_rag_agent.astream(input_data, stream_mode="values"):
        yield event


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/hospital-rag-agent")
async def query_hospital_agent(
    query: HospitalQueryInput,
) -> HospitalQueryOutput:
    
    print("=========== NEW QUERY ===========")
   
    steps = []
    # Run the agent
    async for chunk in stream_agent_with_retry(query.text):
        # Extract the actual text from the last message
        latest_message = chunk["messages"][-1]
        content = latest_message.content

        # Check if the message is a tool call (content is often empty here)
        if not content and hasattr(latest_message, 'tool_calls') and latest_message.tool_calls:
            for tool in latest_message.tool_calls:
                steps.append(f"🔧 Calling tool: `{tool['name']}` with arguments `{tool['args']}`")
        elif content:
            # Try to handle the specific case where GraphRAG returns a JSON string
            display_text = content
            try:
                # If content is a stringified JSON, parse it
                data = json.loads(content)
                if isinstance(data, dict):
                    # Extract the actual answer from the GraphRAG dictionary
                    display_text = data.get("result", data.get("answer", content))
            except (json.JSONDecodeError, TypeError):
                display_text = content

            prefix = "💡 Thought: " if latest_message.type == "ai" else "✅ Result: "
            steps.append(f"{prefix}{display_text}")

    # Ensure we don't crash if steps is empty
    final_output = steps[-1] if steps else "No response generated."
    # Remove the prefix from the final output so the chat bubble looks clean
    clean_output = final_output.replace("✅ Result: ", "").replace("💡 Thought: ", "")
    
    # Return the format FastAPI/Pydantic expects
    return HospitalQueryOutput(
        input=query.text,
        output=clean_output,
        intermediate_steps=steps[1:-1]
    )

