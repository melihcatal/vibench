import os

from openai import OpenAI


def dashboard_note_translate(text: str, target_locale: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(model="gpt-5.4-mini", messages=[{"role": "system", "content": "Translate dashboard notes while preserving metric names and timestamps."}, {"role": "user", "content": f"Translate to {target_locale}: {text}"}])
    return {"translated_text": completion.choices[0].message.content}
