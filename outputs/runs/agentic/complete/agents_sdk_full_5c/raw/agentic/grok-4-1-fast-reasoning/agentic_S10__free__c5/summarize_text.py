from model_client import get_client
from model_models import build_messages, normalize_completion

def summarize_text(text: str, max_tokens: int = 150) -> str:
    client = get_client()
    system = "You are an expert summarizer. Provide a concise and accurate summary of the given text."
    user = f"Summarize this text:\n\n{text}"
    messages = build_messages(system, user)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.3
    )
    return normalize_completion(response)