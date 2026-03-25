from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

PLANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert software architect. Decompose the coding task into clear numbered implementation steps. No code yet."),
    ("human", "Task: {task}\nLanguage: {language}\n\nProvide step-by-step plan:")
])

class PlannerAgent:
    def __init__(self, model="gpt-4o", temperature=0.1):
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.chain = PLANNER_PROMPT | self.llm

    def run(self, state):
        result = self.chain.invoke({"task": state["task"], "language": state.get("language", "python")})
        return {"plan": result.content, "status": "planning", "history": ["[Planner] Generated plan"]}
