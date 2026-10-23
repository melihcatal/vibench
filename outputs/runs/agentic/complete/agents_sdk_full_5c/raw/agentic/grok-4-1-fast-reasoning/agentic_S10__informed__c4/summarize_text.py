from model_client import get_client, MODEL_NAME
from model_models import make_messages, extract_content

def summarize_text(text: str) -> str:
    client = get_client()
    messages = make_messages(
        "You are an expert at summarizing long text concisely while preserving all key information.",
        f"Summarize this text:\n\n{text}"
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.1,
        max_tokens=1000,
    )
    return extract_content(response)
