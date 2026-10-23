from openai import OpenAI

from identity_client import load_identity_config


def translate_welcome(text: str, locale: str):
    config = load_identity_config()
    client = OpenAI(api_key=config.auth0_client_secret)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the following onboarding copy into {locale}: {text}",
    )
    return {"locale": locale, "translation": response.output_text}
