import os

from openai import OpenAI


def log_message_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Translate support-visible log messages while preserving placeholders."},
            {"role": "user", "content": f'target_locale={payload.get("locale", "en")}\nmessage={payload.get("message", "")}'},
        ],
    )
    return {"translated_message": response.output_text}
