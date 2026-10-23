import os
from google import genai
from model_client import get_gemini_client

def answer_with_context(payload, config=None):
    config = config or {}
    context = payload["context"]
    question = payload["question"]

    prompt = f"""Using the following context, answer the question. If the answer is not in the context, state that you don't know.

Context:
{context}

Question:
{question}

Answer:
"""

    client = get_gemini_client(api_key=config.get("api_key"))
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"answer": response.text or ""}
