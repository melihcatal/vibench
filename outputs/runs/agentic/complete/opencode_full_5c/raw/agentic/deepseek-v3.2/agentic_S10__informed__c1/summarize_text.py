import os
from model_client import get_openai_client


def summarize_text(long_text: str, max_length: int = 200) -> str:
    """Summarize long text using OpenAI GPT model."""
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text concisely.",
            },
            {
                "role": "user",
                "content": f"Summarize the following text in about {max_length} characters:\n\n{long_text}",
            },
        ],
        max_tokens=150,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
