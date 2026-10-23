from openai import OpenAI

from identity_models import normalize_locale, normalize_text


def welcome_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    locale = normalize_locale(payload.get("locale"))
    copy = normalize_text(payload.get("copy"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate onboarding copy faithfully and concisely."},
            {"role": "user", "content": f"Locale: {locale}\nCopy: {copy}"},
        ],
    )
    return {"locale": locale, "translated_copy": completion.choices[0].message.content}
