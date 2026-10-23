import json
import os
from model_client import HostedModelClient

def answer_with_context(context: str, question: str, model: str = "gpt-4o") -> str:
    """Answers a question using provided context with a hosted LLM.

    Args:
        context: Background information relevant to the question.
        question: The query to answer.
        model: Model identifier for the hosted LLM provider.

    Returns:
        Answer to the question based on the given context.
    """
    prompt = f"{context}\n
Based on the above context, answer this question:\n{question}"
    client = HostedModelClient(model=model)
    payload = {"prompt": prompt, "temperature": 0.0}
    response = client.chat_completion(payload)
    return response["choices"][0]["message"]["content"]