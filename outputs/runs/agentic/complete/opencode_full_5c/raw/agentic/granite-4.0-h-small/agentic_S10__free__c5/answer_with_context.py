import json
import os
from model_client import HostedLLMClient


def answer_with_context(question: str, context: str) -> str:
    """Answers a question using provided context via a hosted LLM.

    Args:
        question (str): The natural-language question.
        context (str): Relevant background information.

    Returns:
        str: The LLM-generated answer.
    """
    client = HostedLLMClient()
    model = "gpt-4o-mini"
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant answering questions based on the provided context.",
        },
        {"role": "user", "content": f"Question: {question}\nContext:\n{context}"},
    ]
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
    }
    response = client.generate(payload)
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    q = "What is the capital of France?"
    ctxt = "Paris has been the capital of France since 508 AD."
    print("Answer:", answer_with_context(q, ctxt))
