# 🇮🇳 Sarkari Yojana Eligibility Agent

A multi-agent AI system that matches Indian citizens to government schemes (Central + Uttar Pradesh + Maharashtra) based on their profile, explains why they qualify, generates a document checklist, and provides an application guide — all powered by rule-based matching + LLM reasoning.

## Architecture

- **Matching Agent** — Rule-based, deterministic eligibility filtering (7 criteria: occupation, income, age, state, gender, category, disability) against a curated scheme database.
- **Explainer Agent** — Uses Groq (Llama/GPT-OSS) to explain in plain language why a matched scheme fits the user's profile.
- **Checklist Agent** — De-duplicates document requirements across all matched schemes into one combined checklist.
- **Guide Agent** — Generates a step-by-step application guide for each matched scheme.

## Why rule-based matching (not pure LLM)?

Eligibility for government schemes needs to be deterministic and auditable — not left to LLM hallucination. The Matching Agent uses explicit rules; the LLM is only used *after* matching, to explain and guide.

## Privacy Design

Caste/category and disability fields are optional. Schemes that require them but weren't disclosed are still shown as possible matches — the agent never excludes a user just for not disclosing sensitive information.

## Tech Stack

Python, Streamlit, LangChain + Groq API, JSON (curated scheme database)

## Setup

```bash
pip install -r requirements.txt
# create a .env file with: GROQ_API_KEY=your_key_here
python -m streamlit run app.py
```

## Data

`data/schemes.json` has 18 curated schemes (8 central, 5 UP, 5 Maharashtra) sourced from myscheme.gov.in and respective state portals.