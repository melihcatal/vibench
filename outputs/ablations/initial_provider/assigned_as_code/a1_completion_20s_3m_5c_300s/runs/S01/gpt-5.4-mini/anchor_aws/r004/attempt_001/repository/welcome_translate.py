from openai import OpenAI

from identity_models import normalize_locale


def welcome_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    locale = normalize_locale(payload.get("locale") or (config or {}).get("locale"))
    response = client.responses.create(
        model=(config or {}).get("model", "gpt-5.4-mini"),
        input=[
            {"role": "system", "content": "Translate onboarding copy into the target locale."},
            {"role": "user", "content": f'Locale: {locale}\nText: {payload["text"]}'},
        ],
    )
    return {"locale": locale, "translation": response.output_text}
