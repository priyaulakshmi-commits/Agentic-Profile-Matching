from typing import TypedDict
from langgraph.graph import StateGraph, END

from tools import extract_requirements
from rag_search import search_resumes


class AgentState(TypedDict):
    job_description: str
    requirements: dict
    candidates: list
    report: str


def parse_jd(state):
    print("\nParsing Job Description...")
    return state


def extract_node(state):

    requirements = extract_requirements(
        state["job_description"]
    )

    state["requirements"] = requirements

    return state


def search_node(state):

    query = " ".join(
        state["requirements"]["must_have"]
    )

    candidates = search_resumes(query)

    state["candidates"] = candidates

    return state


def report_node(state):

    report = "\nTop Candidates:\n\n"

    for candidate in state["candidates"]:

        report += (
                candidate.metadata["file_name"]
                + "\n"
        )

    state["report"] = report

    print(report)

    return state


graph = StateGraph(AgentState)

graph.add_node("Parse JD", parse_jd)

graph.add_node(
    "Extract Requirements",
    extract_node
)

graph.add_node(
    "Search Resumes",
    search_node
)

graph.add_node(
    "Generate Report",
    report_node
)

graph.set_entry_point("Parse JD")

graph.add_edge(
    "Parse JD",
    "Extract Requirements"
)

graph.add_edge(
    "Extract Requirements",
    "Search Resumes"
)

graph.add_edge(
    "Search Resumes",
    "Generate Report"
)

graph.add_edge(
    "Generate Report",
    END
)

app = graph.compile()