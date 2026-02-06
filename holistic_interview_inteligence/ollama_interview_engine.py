import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def ask_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


def generate_question(role):
    prompt = f"""
You are a technical interviewer.
Ask ONE interview question for a {role}.
Only output the question.
"""
    return ask_llm(prompt)


def analyse_answer(question, answer):
    prompt = f"""
You are an interview coach.

Question: {question}
Candidate Answer: {answer}

Give:
1) Score out of 10
2) What was good
3) What to improve
4) Better sample answer
"""
    return ask_llm(prompt)
