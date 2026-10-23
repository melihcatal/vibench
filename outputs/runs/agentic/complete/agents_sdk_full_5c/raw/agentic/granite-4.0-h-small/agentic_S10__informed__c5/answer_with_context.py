import os
from model_client import LLMClient

def answer_with_context(question: str, context: str, model: str = "gpt-4o-mini") -> str:
    """Answers a question using provided context with a hosted LLM.

    Args:
        question (str): The question to answer.
        context (str): Background information for the model.
        model (str): Model identifier; defaults to OpenAI gpt-4o-mini.

    Returns:
        str: The model's answer.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Given the context below, answer the question: {question}\n\nContext: {context}"
    ]
    client = LLMClient()
    response = client.chat(model=model, messages=messages)
    return response.choices[0].message.content
