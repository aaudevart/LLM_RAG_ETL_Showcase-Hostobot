import os
from typing import Any

import numpy as np
from langchain_neo4j import Neo4jGraph
from langchain.tools import tool

def _get_current_hospitals() -> list[str]:
    
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
    )

    current_hospitals = graph.query(
        """
        MATCH (h:Hospital)
        RETURN h.name AS hospital_name
        """
    )

    current_hospitals = [d["hospital_name"].lower() for d in current_hospitals]

    return current_hospitals


def _get_current_wait_time_minutes(hospital: str) -> int:
    """Get the current wait time at a hospital in minutes."""

    current_hospitals = _get_current_hospitals()

    if hospital.lower() not in current_hospitals:
        return -1

    return np.random.randint(low=0, high=600)
    
@tool("Hospitals", description="""
        Use this tool to fetch a list of current hospital names from a Neo4j database.
        It does not provide historical or aggregated hospital data.
        """
)
def get_current_hospitals_tools() -> list[str]:
    """Fetch a list of current hospital names from a Neo4j database."""
    
    return _get_current_hospitals()


@tool("Waits", description="""
        Use this tool for questions about the current wait time at a specific hospital.
        It only provides real-time wait times and does not support historical or aggregated data.
        Do not include the word “hospital” in the input—only pass the hospital's name.
        For example, if the question is "What is the current wait time at Jordan Inc Hospital?", the input should be: "Jordan Inc".
        """)
def get_current_wait_times(hospital: str) -> str:
    """Get the current wait time at a hospital as a string."""
    
    wait_time_in_minutes = _get_current_wait_time_minutes(hospital)

    if wait_time_in_minutes == -1:
        return f"Hospital '{hospital}' does not exist."

    hours, minutes = divmod(wait_time_in_minutes, 60)

    if hours > 0:
        formatted_wait_time = f"{hours} hours {minutes} minutes"
    else:
        formatted_wait_time = f"{minutes} minutes"

    return formatted_wait_time

@tool("Availability", description="""
        Use this tool to identify the hospital with the shortest current wait time.
        It does not provide historical or aggregated wait time data.
        The tool returns a dictionary where each key is a hospital name and the value is its current wait time in minutes.
        """)
def get_most_available_hospital(_: Any) -> dict[str, float]:
    """Find the hospital with the shortest wait time."""
    
    current_hospitals = _get_current_hospitals()

    current_wait_times = [
        _get_current_wait_time_minutes(h) for h in current_hospitals
    ]

    best_time_idx = np.argmin(current_wait_times)
    best_hospital = current_hospitals[best_time_idx]
    best_wait_time = current_wait_times[best_time_idx]

    return {best_hospital: best_wait_time}
