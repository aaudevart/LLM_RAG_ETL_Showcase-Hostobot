import os

from chains.hospital_cypher_chain import hospital_cypher_chain
from chains.hospital_review_chain import reviews_vector_chain
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from tools.wait_times import (
    get_current_wait_times,
    get_most_available_hospital,
    get_current_hospitals_tools
)
from typing import Any

HOSPITAL_AGENT_PROVIDER = os.getenv("HOSPITAL_AGENT_PROVIDER")
HOSPITAL_AGENT_MODEL = os.getenv("HOSPITAL_AGENT_MODEL")

@tool("Experiences", description= """
        Use this tool when addressing questions about patient experiences, emotions, or other qualitative aspects that can be answered through semantic search.
        It is not appropriate for objective questions involving counts, percentages, aggregations, or factual listings.
        Always provide the entire prompt as the input: for example, if the question is "Are patients satisfied with their care?", then the input should be exactly: "Are patients satisfied with their care?"
        """)
def get_reviews(question: Any) -> str:
    """Use this tool when addressing questions about patient experiences, emotions, or other qualitative aspects that can be answered through semantic search."""
    return reviews_vector_chain.invoke(question)

@tool("Graph", description="""
        Best suited for answering questions related to patients, physicians, hospitals, insurance payers, patient review metrics, and hospital visit details.
        Always provide the full prompt as input : for example, if the question is "How many visits have there been?", then the input should be exactly: "How many visits have there been?
        """)
def get_graph(question: Any) -> str:
    print("get_graph")
    print(question)
    return hospital_cypher_chain.invoke(question)

chat_model = init_chat_model(model_provider=HOSPITAL_AGENT_PROVIDER,
                             model=HOSPITAL_AGENT_MODEL,
                             temperature=0)


hospital_rag_agent = create_agent(
    model=chat_model,
    system_prompt="You are a helpful assistant",
    tools=[get_current_wait_times, get_most_available_hospital, get_reviews, get_graph, get_current_hospitals_tools],
)
