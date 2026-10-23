from model_client import get_llm_client
from model_models import build_messages, normalize_chat_response

def answer_with_context(question: str, context: str) -> str:
    client = get_llm_client()
    system_prompt = "You are a helpful assistant. Answer the question based only on the provided context. If the answer is not in the context, say 'I don't know'."
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"
    messages = build_messages(system_prompt, user_prompt)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1
    )
    return normalize_chat_response(response)