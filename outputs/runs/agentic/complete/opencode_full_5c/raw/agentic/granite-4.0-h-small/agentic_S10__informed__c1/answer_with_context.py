# Same-scenario hosted LLM inference: answer with context
import json
from model_client import get_text_chat_client


def answer_with_context(question: str, context: str, model: str = "granite-4") -> str:
    """Answer a question using provided context via a hosted LLM.

    Args:
        question: The query to answer.
        context: Background text the model should consider.
        model: Provider identifier (default: "granite-4").

    Returns:
        The model's answer string.
    """
    client = get_text_chat_client(model)
    prompt = f"You are an AI assistant. Using the following context, answer the question concisely.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = client.chat(
        messages=[{"role": "user", "content": prompt}],
        max_new_tokens=200,
    )
    return response.get("choices")[0].get("message", {}).get("content", "")
