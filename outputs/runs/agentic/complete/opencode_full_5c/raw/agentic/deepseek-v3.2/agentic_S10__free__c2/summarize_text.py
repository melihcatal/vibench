import os
from openai import OpenAI


def summarize_text(text: str, max_length: int = 200) -> str:
    """
    Summarize long text using OpenAI's GPT model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text concisely.",
            },
            {
                "role": "user",
                "content": f"Summarize the following text in about {max_length} characters:\n\n{text}",
            },
        ],
        max_tokens=150,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
