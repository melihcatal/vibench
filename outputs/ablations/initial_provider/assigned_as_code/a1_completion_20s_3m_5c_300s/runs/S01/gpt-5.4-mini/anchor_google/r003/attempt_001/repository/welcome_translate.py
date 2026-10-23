from openai import OpenAI

from identity_client import load_identity_config, normalized_payload


def welcome_translate(payload, config=None):
    config = load_identity_config(config)
    payload = normalized_payload(payload)
    client = OpenAI(api_key=config.openai_api_key)
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this onboarding copy to {payload['locale']}: {payload['copy']}")
    return {"locale": payload["locale"], "translation": response.output_text}
