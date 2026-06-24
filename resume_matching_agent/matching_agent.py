from typing import TypedDict
from langgraph.graph import StateGraph, END

from tools import extract_requirements
from rag_search import search_resumes


class AgentState(TypedDict):
    job_description: str
    requirements: dict
    candidates: list
    ranked_candidates: list
    report: str
    feedback: str


def parse_jd(state):
    print("\nParsing Job Description...")
    return state


def extract_node(state):
    requirements = extract_requirements(
        state["job_description"]
    )

    state["requirements"] = requirements

    print("\nRequirements Extracted:")
    print(requirements)

    return state


def search_node(state):
    query = " ".join(
        state["requirements"]["must_have"]
    )

    print("\nSearching Resumes...")
    print("Query:", query)

    candidates = search_resumes(query)

    state["candidates"] = candidates

    print("\nCandidates Found:")

    for candidate in candidates:
        print(candidate.metadata["file_name"])

    return state
def rank_candidates_node(state):

    ranked = []

    for candidate in state["candidates"]:

        score = 0

        resume_text = candidate.page_content.lower()

        for skill in state["requirements"]["must_have"]:
            if skill.lower() in resume_text:
                score += 10

        for skill in state["requirements"]["nice_to_have"]:
            if skill.lower() in resume_text:
                score += 5

        ranked.append({
            "candidate": candidate.metadata["file_name"],
            "score": score
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    state["ranked_candidates"] = ranked

    print("\nCandidate Rankings:")

    for candidate in ranked:
        print(
            f"{candidate['candidate']} "
            f"Score: {candidate['score']}"
        )

    return state

def report_node(state):

    report = "\n===== Candidate Ranking Report =====\n\n"

    for idx, candidate in enumerate(
            state["ranked_candidates"],
            start=1
    ):

        report += (
            f"{idx}. "
            f"{candidate['candidate']} "
            f"(Score: {candidate['score']})\n"
        )

    state["report"] = report

    print(report)

    return state

def feedback_node(state):

    feedback = input(
        "\nAny additional requirements? "
        "(Press Enter to skip): "
    )

    state["feedback"] = feedback

    if feedback:
        print(
            f"\nFeedback received: {feedback}"
        )

    return state


graph = StateGraph(AgentState)

graph.add_node("Parse JD", parse_jd)
graph.add_node("Extract Requirements", extract_node)
graph.add_node("Search Resumes", search_node)
graph.add_node(
    "Rank Candidates",
    rank_candidates_node
)
graph.add_node(
    "Generate Report",
    report_node
)
graph.add_node(
    "Human Feedback",
    feedback_node
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
    "Rank Candidates"
)

graph.add_edge(
    "Rank Candidates",
    "Generate Report"
)

graph.add_edge(
    "Generate Report",
    "Human Feedback"
)

graph.add_edge(
    "Human Feedback",
    END
)

app = graph.compile()