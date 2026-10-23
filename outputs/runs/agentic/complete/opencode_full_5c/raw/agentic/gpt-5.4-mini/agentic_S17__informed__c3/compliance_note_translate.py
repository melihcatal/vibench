import os

from openai import OpenAI


def compliance_note_translate(text, target_language):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate this compliance note to {target_language}: {text}"
    result = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )
    return result.choices[0].message.content
