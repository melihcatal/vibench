import os
from model_client import get_chat_client
from model_models import format_chat_response

def answer_with_context(question: str, context: str, model: str = "gpt-4o") -> str:
    """Answer a question using provided context via a hosted LLM.

    Args:
        question (str): The question to answer.
        context (str): Background text the model can use.
        model (str): Model identifier (default GPT-4o).
    """
    client = get_chat_client(model)
    messages = [
        {"role": "user", "content": f"{context}\n\n{question}"},
    ]
    response = client.chat(messages=messages, temperature=0.2)
    return format_chat_response(response)
