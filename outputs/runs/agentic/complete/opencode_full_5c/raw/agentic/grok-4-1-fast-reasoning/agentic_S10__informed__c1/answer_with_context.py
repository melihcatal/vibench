from model_client import get_llm_client
from model_models import (
    MODEL_FAMILY,
    create_system_message,
    create_user_message,
    normalize_response,
    DEFAULT_PARAMS,
)


def answer_with_context(question: str, context: str) -> str:
    client = get_llm_client()
    messages = [
        create_system_message(
            "You are a helpful assistant. Answer the question using only the provided context. If the answer is not in the context, say 'I don't know'."
        ),
        create_user_message(f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"),
    ]
    response = client.chat(model=MODEL_FAMILY, messages=messages, **DEFAULT_PARAMS)
    return normalize_response(response)
