from openai import OpenAI

from security_models import normalize_secret_value


def rotation_summary(notes: str, model: str = "gpt-5.4-mini"):
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": normalize_secret_value(notes)}],
    )
    return response.choices[0].message.content
