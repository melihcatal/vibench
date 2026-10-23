import os

from openai import OpenAI


def record_translate(text, target_language="es"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate the following text to {target_language}: {text}"
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
