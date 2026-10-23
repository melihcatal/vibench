import os

from openai import OpenAI


def dashboard_note_translate(text, locale, model="gpt-5.4-mini"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Translate this dashboard note to {locale}: {text}",
            }
        ],
    )
    return response.choices[0].message.content
