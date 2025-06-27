import streamlit as st
from advisor import get_chat_response
from resume_parser import extract_resume_data
import tempfile
import os

st.set_page_config(page_title="AI Career Advisor Chatbot", layout="centered")
st.title("💬 AI Career Advisor Chatbot")

st.markdown("""
You can upload your resume and then chat with the AI Career Advisor!
Ask questions like:
- What are the best roles for my skills?
- Suggest courses I should take.
- What companies hire for my background?
""")

# Upload resume
resume_file = st.file_uploader("📄 Upload Your Resume (PDF) - Optional", type=["pdf"])
resume_context = ""

if resume_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(resume_file.read())
        tmp_path = tmp.name
    extracted = extract_resume_data(tmp_path)
    os.unlink(tmp_path)

    resume_context = f"""
User Background:
- Education: {extracted.get("education", "")}
- Skills: {extracted.get("skills", "")}
- Interests: {extracted.get("interests", "")}
"""
    st.success("✅ Resume uploaded and parsed successfully!")
    st.markdown("**You can now start chatting with the AI Career Advisor.**")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    if resume_context:
        st.session_state.chat_history.append({"role": "system", "content": resume_context})

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking... 💡"):
        response = get_chat_response(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Display chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
