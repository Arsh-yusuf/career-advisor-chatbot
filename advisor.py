# advisor.py (Chatbot support with memory)
import cohere
import os
import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.base import LLM

# Get API key (works for both local + Streamlit Cloud)
if "COHERE_API_KEY" in st.secrets:
    COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
else:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(COHERE_API_KEY)

# Cohere LangChain-compatible wrapper (still optional)
class CohereLLM(LLM):
    def _call(self, prompt, stop=None):
        response = co.chat(
            model="command-a-03-2025",  # ✅ New Chat API model
            message=prompt,
            temperature=0.6
        )
        return response.text.strip()

    @property
    def _llm_type(self):
        return "cohere"

# Persistent memory
memory = ConversationBufferMemory(return_messages=True)
llm = CohereLLM()
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

def get_chat_response(user_input, history):
    background = ""
    for msg in history:
        if msg["role"] == "system":
            background = msg["content"]
            break

    chat_context = ""
    for msg in history:
        if msg["role"] != "system":
            prefix = "User" if msg["role"] == "user" else "AI"
            chat_context += f"{prefix}: {msg['content']}\n"

    prompt = f"""
    {background}

    You are an AI Career Advisor. Use the user's background to provide detailed, role-specific, and course-based suggestions.

    {chat_context}
    AI:"""

    # ✅ Use the new free-tier model (Chat API)
    response = co.chat(
        model="c4",           # <-- free-tier compatible model
        message=prompt,
        temperature=0.7
    )

    return response.text.strip()

def get_career_advice(name, education, skills, interests):
    prompt = f"""
    You are an AI Career Advisor.
    The user is named {name} and has the following background:
    - Education: {education}
    - Skills: {skills}
    - Interests: {interests}

    Suggest 3 suitable career paths for this user.
    For each path, recommend 2 relevant online courses and 3 top companies hiring in that field.
    """

    response = co.chat(
        model="command-r",
        message=prompt,
        temperature=0.6
    )

    return response.text.strip()

# ✅ Structured career advice generator
def get_career_advice(name, education, skills, interests):
    prompt = f"""
    You are an AI Career Advisor.
    The user is named {name} and has the following background:
    - Education: {education}
    - Skills: {skills}
    - Interests: {interests}

    Suggest 3 suitable career paths for this user. 
    For each path, recommend 2 relevant online courses and list 3 top companies hiring in that field.
    """

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=500,
        temperature=0.6
    )
    return response.generations[0].text.strip()




