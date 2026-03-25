from __future__ import annotations
import operator
from typing import Annotated, List, Optional, TypedDict
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

class CodeState(TypedDict):
    task: str
    language: str
    plan: Optional[str]
    code: Optional[str]
    execution_output: Optional[str]
    execution_error: Optional[str]
    debug_analysis: Optional[str]
    test_code: Optional[str]
    test_results: Optional[str]
    final_code: Optional[str]
    retry_count: int
    max_retries: int
    history: Annotated[List[str], operator.add]
    status: str

def should_debug_or_finish(state):
    if state.get("execution_error"):
        if state["retry_count"] >= state["max_retries"]:
            return "failed"
        return "debug"
    return "test"

def build_coding_graph(planner, coder, executor, debugger, tester):
    workflow = StateGraph(CodeState)
    workflow.add_node("planner", planner.run)
    workflow.add_node("coder", coder.run)
    workflow.add_node("executor", executor.run)
    workflow.add_node("debugger", debugger.run)
    workflow.add_node("tester", tester.run)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "coder")
    workflow.add_edge("coder", "executor")
    workflow.add_conditional_edges("executor", should_debug_or_finish, {"debug": "debugger", "test": "tester", "failed": END})
    workflow.add_edge("debugger", "coder")
    workflow.add_edge("tester", END)
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)
