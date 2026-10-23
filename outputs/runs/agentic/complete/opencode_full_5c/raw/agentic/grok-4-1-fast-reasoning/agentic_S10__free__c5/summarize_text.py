from model_client import openai_client
from model_models import parse_openai_chat


def summarize_text(text: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Summarize the following text concisely and accurately.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0.1,
        max_tokens=500,
    )
    return parse_openai_chat(response)
