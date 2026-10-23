from openai import OpenAI

from identity_models import load_identity_config, normalize_text_payload


def welcome_translate(payload, config=None):
    config = load_identity_config(config)
    payload = normalize_text_payload(payload)
    client = OpenAI(api_key=config["openai_api_key"])
    completion = client.chat.completions.create(
        model=config["openai_model"],
        messages=[
            {"role": "system", "content": "Translate onboarding copy into the target locale while preserving meaning."},
            {"role": "user", "content": f"Locale: {payload['locale']}\nText: {payload['text']}"},
        ],
    )
    return {"translated_text": completion.choices[0].message.content}
