# answer_with_context.py
# [SAME-SCENARIO]
"""Calls a hosted LLM to answer a natural language question using a given context."""

from model_client import LLMClient


def answer_with_context(question: str, context: str, model: str = "gpt-4o-mini") -> str:
    """Answers a question using the provided context via a hosted model.

    Args:
        question (str): The natural language question.
        context (str): Background text to ground the answer.
        model (str): Identifier of the hosted model to use.
    Returns:
        str: The generated answer.
    """
    client = LLMClient(model=model)
    prompt = f"You are an expert assistant. Using the context below, answer the question concisely (max 2 sentences).\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = client.chat(messages=[{"role": "user", "content": prompt}])
    return response["choices"][0]["message"]["content"]
