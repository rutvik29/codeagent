from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

CODER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {language} developer. Write clean, production-quality code with type hints, docstrings, and error handling. Return ONLY code."),
    ("human", "Task: {task}\n\nPlan:\n{plan}\n\n{debug_context}\n\nWrite implementation:")
])

class CoderAgent:
    def __init__(self, model="gpt-4o", temperature=0.0):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.chain = CODER_PROMPT | self.llm

    def run(self, state):
        debug_ctx = f"Fix these issues:\n{state['debug_analysis']}" if state.get("debug_analysis") else ""
        result = self.chain.invoke({"task": state["task"], "language": state.get("language","python"), "plan": state.get("plan",""), "debug_context": debug_ctx})
        retry = state.get("retry_count", 0) + (1 if state.get("execution_error") else 0)
        return {"code": result.content, "retry_count": retry, "execution_error": None, "status": "coding", "history": [f"[Coder] attempt {retry+1}"]}
