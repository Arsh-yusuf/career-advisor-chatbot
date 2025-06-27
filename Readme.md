# AI Career Advisor Chatbot

This is an AI-powered chatbot built using Streamlit, LangChain, and Cohere's large language models. It helps users explore career paths based on their resume or natural language conversation.

---

## 💡 Features
- Upload your resume PDF for auto-parsing
- Extracts education, skills, and interests
- Chatbot-style interaction using LLM
- Suggests career roles, courses, and companies
- Deployed easily via Streamlit Cloud

---

## 📁 Project Structure
```
career-advisor-chatbot/
├── app.py                # Streamlit app with chat + resume support
├── advisor.py            # Cohere + LangChain logic
├── resume_parser.py      # Resume section extractor
├── requirements.txt      # Pip dependencies
├── .streamlit/
│   └── secrets.toml      # For deployment (Streamlit Cloud)
├── .gitignore            # Prevents .env and cache from being committed
├── README.md             # You're reading it 🙂
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/career-advisor-chatbot.git
cd career-advisor-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```



### 4. Run locally
```bash
streamlit run app.py
```

## 📸 Sample Interaction
> **User:** I just graduated in AI with Python and ML experience. What careers suit me?
>
> **AI:** You could consider roles like:
> - Machine Learning Engineer
> - AI Research Associate
> - Data Scientist
> With courses like...

--
---

