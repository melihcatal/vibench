import os
from openai import OpenAI


def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (OpenAI) to summarize long text.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Provider-specific model ID
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {"role": "user", "content": f"Summarize the following text: {text}"},
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()
