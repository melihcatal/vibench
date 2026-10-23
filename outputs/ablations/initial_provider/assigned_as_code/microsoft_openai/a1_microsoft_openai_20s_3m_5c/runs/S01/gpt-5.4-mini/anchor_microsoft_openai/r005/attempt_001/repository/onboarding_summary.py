from openai import OpenAI

from identity_client import load_identity_config


def onboarding_summary(payload, config=None):
    config = load_identity_config(config)
    payload = payload or {}
    client = OpenAI(api_key=config.openai_api_key)
    response = client.responses.create(model='gpt-5.4-mini', input=f"Summarize onboarding state for support: {payload}")
    return {'summary': response.output_text}
