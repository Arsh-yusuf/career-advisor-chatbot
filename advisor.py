# advisor.py (Chatbot support with memory)
import cohere
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.base import LLM
import streamlit as st

# For local development

# from dotenv import load_dotenv
# load_dotenv()  # Load .env variables

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# co = cohere.Client(COHERE_API_KEY)

COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
co = cohere.Client(COHERE_API_KEY)

# Basic wrapper for Cohere as a LangChain-compatible LLM
class CohereLLM(LLM):
    def _call(self, prompt, stop=None):
        response = co.generate(prompt=prompt, model="command", max_tokens=400, temperature=0.6)
        return response.generations[0].text.strip()

    @property
    def _llm_type(self):
        return "cohere"

# Persistent memory
memory = ConversationBufferMemory(return_messages=True)
llm = CohereLLM()
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

def get_chat_response(user_input, history):
    # Extract resume background (system message)
    background = ""
    for msg in history:
        if msg["role"] == "system":
            background = msg["content"]
            break

    # Combine background + full chat history as context
    conversation = ""
    for msg in history:
        if msg["role"] != "system":
            prefix = "User" if msg["role"] == "user" else "AI"
            conversation += f"{prefix}: {msg['content']}\n"

    # Final prompt
    prompt = f"""{background}

You are an AI Career Advisor. Use the user's background to provide helpful, role-specific, and course-based suggestions.

{conversation}
AI:"""

    response = co.generate(
        model="command",  # or "command-light"
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )

    return response.generations[0].text.strip()


def get_career_advice(name, education, skills, interests):
    prompt = f"""
    You are an AI Career Advisor.
    The user is named {name} and has the following background:
    - Education: {education}
    - Skills: {skills}
    - Interests: {interests}

    Suggest 3 suitable career paths for this user. For each path, recommend 2 online courses and top companies hiring in that field.
    """
    response = co.generate(model="command", prompt=prompt, max_tokens=500, temperature=0.6)
    return response.generations[0].text.strip()
