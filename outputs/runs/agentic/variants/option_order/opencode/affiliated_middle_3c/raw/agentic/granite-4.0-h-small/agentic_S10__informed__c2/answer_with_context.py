# Answer a question using provided context via DashScope Qwen API
import os
from dashscope import text
from model_client import get_dashscope_client


def answer_with_context(question: str, context: str, model: str = "qwen-plus") -> str:
    """Answer a question using context using DashScope Qwen model.

    Args:
        question (str): The question to answer.
        context (str): Background information for the answer.
        model (str): Qwen model identifier (default: "qwen-plus").

    Returns:
        str: The generated answer.
    """
    prompt = f"You are an AI assistant. Use the following context to answer the question below:\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer in a concise manner."
    client = get_dashscope_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content
