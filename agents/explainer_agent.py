import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY")

)

def explain_eligibility(scheme, profile):
    prompt = f"""You are helping a citizen understand why they quality for a government scheme.
    
    Scheme: {scheme['name']}
    Description: {scheme['description']}
    Eligibility criteria: {scheme['eligibility']}

    User profile: {profile}

    In 2-3 short sentence, explain in simple language why this user likely qualifies for this scheme.Respond in Hinglish (mix of Hindi and English)."""

    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    from matching_agent import match_schemes

    sample_profile = {"occupation": "farmer", "income": 200000, "age": 25, "state": "Uttar Pradesh", "gender": "male"}
    results = match_schemes(sample_profile)

    for scheme in results:
        explanation = explain_eligibility(scheme, sample_profile)
        print(f"\n{scheme['name']}:")
        print(explanation)