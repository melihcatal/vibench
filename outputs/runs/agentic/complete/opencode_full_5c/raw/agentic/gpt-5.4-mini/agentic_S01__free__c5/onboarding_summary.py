from openai import OpenAI

from identity_client import load_identity_config


def summarize_onboarding(state: str):
    config = load_identity_config()
    client = OpenAI(api_key=config.auth0_client_secret)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize this onboarding state for support: {state}",
    )
    return {"summary": response.output_text}
