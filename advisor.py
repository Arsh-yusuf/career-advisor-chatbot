# advisor.py (Chatbot support with memory)
import cohere
import os
import streamlit as st

# ✅ Updated LangChain imports (new modular structure)
from langchain_community.chains import ConversationChain
from langchain_community.memory import ConversationBufferMemory
from langchain_core.language_models.llms import LLM  # updated import

# Get Cohere API key (supports both local and Streamlit Cloud)
if "COHERE_API_KEY" in st.secrets:
    COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
else:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

co = cohere.Client(COHERE_API_KEY)

# ✅ Define LangChain-compatible Cohere wrapper
class CohereLLM(LLM):
    def _call(self, prompt, stop=None):
        response = co.generate(
            prompt=prompt,
            model="command",  # You can also use "command-r" or "command-light"
            max_tokens=400,
            temperature=0.6
        )
        return response.generations[0].text.strip()

    @property
    def _llm_type(self):
        return "cohere"

# ✅ Initialize memory and conversation
memory = ConversationBufferMemory(return_messages=True)
llm = CohereLLM()
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

# ✅ Chat response with memory
def get_chat_response(user_input, history):
    background = ""
    for msg in history:
        if msg["role"] == "system":
            background = msg["content"]
            break

    # Combine chat context
    chat_context = ""
    for msg in history:
        if msg["role"] != "system":
            prefix = "User" if msg["role"] == "user" else "AI"
            chat_context += f"{prefix}: {msg['content']}\n"

    prompt = f"""
    {background}

    You are an AI Career Advisor. Use the user's background to provide role-specific and course-based suggestions.

    {chat_context}
    AI:"""

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.generations[0].text.strip()

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
