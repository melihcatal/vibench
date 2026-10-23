from model_client import client


def answer_with_context(question: str, context: str) -> str:
    response = client.answer_with_context(question, context)
    return response.text
