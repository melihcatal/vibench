import json
from model_client import create_client


def answer_with_context(context: str, question: str, model: str = "gpt-4o-mini") -> str:
    """Answer a question using provided context with a hosted LLM.

    Args:
        context (str): Background information for the question.
        question (str): The question to answer.
        model (str): The model family to use (default: gpt-4o-mini).

    Returns:
        str: The LLM's answer.
    """
    client = create_client(model)
    prompt = f"Use the following context to answer the question. Respond with just the answer, nothing else:\n\nContext: {context}\nQuestion: {question}"
    response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content.strip()
