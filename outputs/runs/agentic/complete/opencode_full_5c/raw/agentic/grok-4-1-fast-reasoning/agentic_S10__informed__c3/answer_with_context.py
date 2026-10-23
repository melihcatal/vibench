from model_client import get_openai_client, get_model
from model_models import build_chat_messages, normalize_completion_response


def answer_with_context(question: str, context: str) -> str:
    client = get_openai_client()
    model = get_model()
    system_prompt = "Answer questions accurately using only the provided context. If the answer is not in the context, say so."
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    messages = build_chat_messages(system_prompt=system_prompt, user_prompt=user_prompt)
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0.1
    )
    return normalize_completion_response(response)
