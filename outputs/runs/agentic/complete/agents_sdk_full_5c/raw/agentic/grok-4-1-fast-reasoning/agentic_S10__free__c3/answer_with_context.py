from model_client import get_llm_client
from model_models import build_system_user_prompt, normalize_completion

def answer_with_context(context: str, question: str) -> str:
    client = get_llm_client()
    system_prompt = """You are a helpful assistant. Answer the question based ONLY on the provided context.
If the answer cannot be found in the context, respond with "I don't know.""""
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    messages = build_system_user_prompt(system_prompt, user_prompt)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
        temperature=0.1
    )
    return normalize_completion(response)