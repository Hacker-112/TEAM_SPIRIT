import os
from google import genai

# Create Gemini client using API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.0-flash"   # ⭐ New working model

# 1️⃣ Generate Interview Question
def generate_question(role="Python Developer"):
    prompt = f"""
You are a professional interviewer.
Ask ONE technical interview question for a {role}.
Return only the question.
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text.strip()


# 2️⃣ Analyze Candidate Answer
def analyze_answer(question, answer):
    prompt = f"""
Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer:
• Score out of 10
• Strengths
• Weaknesses
• Final verdict
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text.strip()


# 3️⃣ Improve Answer
def improve_answer(question, answer):
    prompt = f"""
Interview Question:
{question}

Candidate Answer:
{answer}

Write a strong ideal interview answer.
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text.strip()
