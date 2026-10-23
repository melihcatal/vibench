from model_client import client
from model_models import extract_completion_content

def summarize_text(long_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Please provide a concise summary of the following text:\n\n{long_text}"}
        ],
        max_tokens=500,
        temperature=0.3,
    )
    return extract_completion_content(response)