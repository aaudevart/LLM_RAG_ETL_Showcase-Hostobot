from agents.hospital_rag_agent import hospital_rag_agent
from fastapi import FastAPI
from models.hospital_rag_query import HospitalQueryInput, HospitalQueryOutput
from utils.async_utils import async_retry_generator


app = FastAPI(
    title="Hospital Chatbot",
    description="Endpoints for a hospital system graph RAG chatbot",
)

@async_retry_generator(max_retries=3, delay=1)
async def stream_agent_with_retry(query: str):
    """
    Stream the agents events with a retry logic.
    """
    input_data = {"messages": [{"role": "user", "content": query}]}
    
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
        steps.append(latest_message.content)
        print(f"==> Message ({latest_message.type}): {latest_message.content}")

    
    # Return the format FastAPI/Pydantic expects
    return HospitalQueryOutput(
        input=query.text,
        output=steps[-1],
        intermediate_steps=steps[:-1]
    )
    
