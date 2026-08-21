import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def generate_guide(scheme):
    prompt = f"""You are helping a citizen apply for a government scheme.

Scheme: {scheme['name']}
Description: {scheme['description']}
Apply link: {scheme['apply_link']}

Give a short 3-4 step application guide in simple Hinglish. Include whether it's online or offline, and one practical tip."""

    response = llm.invoke(prompt)
    return response.content