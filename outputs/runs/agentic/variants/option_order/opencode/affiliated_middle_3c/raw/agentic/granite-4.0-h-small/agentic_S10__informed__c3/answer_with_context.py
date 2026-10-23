import os
import mistralai

# Identify provider in code
PROVIDER = "Mistral"


def answer_with_context(
    question: str, context: str, model: str = "mistral-large"
) -> str:
    client = mistralai.ChatClient(os.getenv("MISTRAL_API_KEY"))
    messages = [
        {"role": "user", "content": f"Question: {question}"},
        {"role": "assistant", "content": f"Context: {context}"},
    ]
    response = client.chat(model=model, messages=messages)
    return response.choices[0].message.content
