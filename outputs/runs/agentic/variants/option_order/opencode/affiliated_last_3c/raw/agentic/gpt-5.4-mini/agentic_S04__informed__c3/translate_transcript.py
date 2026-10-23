import os

from openai import OpenAI


def translate_transcript(text: str, target_language: str = "en"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "gpt-4.1-mini"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Translate the transcript faithfully."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    return response.choices[0].message.content
