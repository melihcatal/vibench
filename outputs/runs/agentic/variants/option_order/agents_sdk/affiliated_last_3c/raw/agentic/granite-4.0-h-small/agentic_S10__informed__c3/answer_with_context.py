# [SAME-SCENARIO] answer_with_context.py

import os
from model_client import HostedLLMClient

def answer_with_context(question: str, context: str, model_family: str = "gpt-4") -> str:
    """Answer a question using provided context via a hosted LLM.

    Args:
        question (str): The question to answer.
        context (str): Background information.
        model_family (str): Provider identifier.

    Returns:
        str: Answer to the question.
    """
    client = HostedLLMClient(model_family=model_family)
    prompt = f"You must answer ONLY the question using the context provided.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:" 
    response = client.complete(prompt=prompt)
    return response['choices'][0]['text'].strip()
