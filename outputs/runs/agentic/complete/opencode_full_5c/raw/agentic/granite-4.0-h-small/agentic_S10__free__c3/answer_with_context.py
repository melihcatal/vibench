import json
from model_client import ModelClient


def answer_with_context(
    question: str, context: str, model_name: str = "gpt-4o-mini"
) -> str:
    """Answer a question using provided context via a hosted LLM.

    Args:
        question (str): The query to answer.
        context (str): The background information for context-aware answering.
        model_name (str): Hosted model identifier (default: gpt-4o-mini).

    Returns:
        str: The LLM-generated answer.
    """
    client = ModelClient(model_name)
    prompt = f"Given this context, answer the question concisely:\n\nContext: {context}\n\nQuestion: {question}"
    response = client.complete(prompt)
    return response["text"].strip()
