from model_client import get_client
from model_models import build_messages, normalize_completion

def answer_with_context(context: str, question: str) -> str:
    client = get_client()
    system = "You are a helpful assistant. Answer the question using only the provided context. If the answer is not in the context, say 'Information not available in context.'"
    user = f"Context:\n{context}\n\nQuestion: {question}"
    messages = build_messages(system, user)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1
    )
    return normalize_completion(response)