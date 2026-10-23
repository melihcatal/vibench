import os

from openai import OpenAI


def invoice_note_translate(text, target_language="en"):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": f"Translate to {target_language}: {text}"}
        ],
    )
    return response.choices[0].message.content
