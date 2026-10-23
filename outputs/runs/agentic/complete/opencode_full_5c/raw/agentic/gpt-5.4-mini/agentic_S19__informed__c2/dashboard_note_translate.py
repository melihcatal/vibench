from openai import OpenAI


def dashboard_note_translate(text: str, locale: str):
    client = OpenAI()
    return client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": f"Translate metric or dashboard notes to {locale}."},
            {"role": "user", "content": text},
        ],
    )
