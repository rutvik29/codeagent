import streamlit as st, requests

st.set_page_config(page_title="CodeAgent", page_icon="🤖", layout="wide")
st.title("🤖 CodeAgent — Autonomous Coding Assistant")

with st.sidebar:
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])
    language = st.selectbox("Language", ["python", "javascript", "typescript", "go"])
    max_retries = st.slider("Max debug retries", 1, 5, 3)
    api_url = st.text_input("API URL", "http://localhost:8001")

task = st.text_area("Coding Task", placeholder="e.g. Write a function to merge k sorted lists using a min-heap with full pytest tests.", height=120)

if st.button("🚀 Generate Code", type="primary") and task:
    with st.spinner("Agent planning & coding..."):
        try:
            resp = requests.post(f"{api_url}/generate", json={"task": task, "language": language, "max_retries": max_retries, "model": model}, timeout=120)
            result = resp.json()
            st.code(result.get("final_code", str(result)), language=language)
        except Exception as e:
            st.error(f"Error: {e}")
