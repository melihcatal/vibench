import os
from model_client import get_llm_client
from model_models import InferenceResponse

def answer_with_context(question: str, context: str, model_family: str = "gpt-4") -> str:
    """Answer a question using provided context via a hosted LLM.

    Args:
        question: The natural‑language question.
        context: Background information the model should consider.
        model_family: LLM family/model identifier (default: "gpt-4").

    Returns:
        The model's answer to the question.
    """
    client = get_llm_client(model_family)
    payload = {
        "model": model_family,
        "prompt": f"Answer the question using the context below. Provide a concise answer:\n\nQuestion: {question}\nContext: {context}",
        "temperature": 0.3,
    }
    response = client.chat_completion(payload)  # type: ignore
    answer = response.choices[0].message.content.strip()
    return answer
