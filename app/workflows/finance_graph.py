from langgraph.graph import StateGraph, END
from app.workflows.finance_state import FinanceAgentState
from app.workflows.finance_nodes import (
    investigation_node,
    route_decision,
    approve_node,
    review_node,
    escalate_node,
    manual_investigation_node,
    retry_node,
)


def build_finance_graph():
    graph = StateGraph(FinanceAgentState)

    graph.add_node("investigation", investigation_node)
    graph.add_node("approve_path", approve_node)
    graph.add_node("review_path", review_node)
    graph.add_node("escalate_path", escalate_node)
    graph.add_node("manual_investigation_path", manual_investigation_node)
    graph.add_node("retry_path", retry_node)

    graph.set_entry_point("investigation")

    graph.add_conditional_edges(
        "investigation",
        route_decision,
        {
            "approve_path": "approve_path",
            "review_path": "review_path",
            "escalate_path": "escalate_path",
            "manual_investigation_path": "manual_investigation_path",
            "retry_path": "retry_path",
        },
    )

    graph.add_edge("approve_path", END)
    graph.add_edge("review_path", END)
    graph.add_edge("escalate_path", END)
    graph.add_edge("manual_investigation_path", END)
    graph.add_edge("retry_path", END)

    return graph.compile()