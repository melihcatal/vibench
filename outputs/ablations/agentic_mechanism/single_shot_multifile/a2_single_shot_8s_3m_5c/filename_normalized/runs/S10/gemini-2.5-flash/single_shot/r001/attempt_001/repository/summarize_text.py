from model_client import get_openai_client
from model_models import normalize_response

def summarize_text(text: str, max_tokens: int = 150) -> str:
    client = get_openai_client()
    model_id = "gpt-4o"
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    normalized = normalize_response(response, "openai")
    return normalized.get("text", "")