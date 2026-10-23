import os
import requests

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def answer_with_context(question, context):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {
                "role": "user",
                "content": f"Answer the following question using the provided context: {question}. Context: {context}",
            }
        ],
    }
    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions", headers=headers, json=data
    )
    return response.json()["choices"][0]["message"]["content"]
