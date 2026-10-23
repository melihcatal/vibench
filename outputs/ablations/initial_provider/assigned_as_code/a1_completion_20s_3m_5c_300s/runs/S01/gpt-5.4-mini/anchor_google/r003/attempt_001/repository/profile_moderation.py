from openai import OpenAI

from identity_client import load_identity_config, normalized_payload


def profile_moderation(payload, config=None):
    config = load_identity_config(config)
    payload = normalized_payload(payload)
    client = OpenAI(api_key=config.openai_api_key)
    response = client.moderations.create(model="omni-moderation-latest", input=payload["profile_text"])
    result = response.results[0]
    return {"flagged": result.flagged, "categories": dict(result.categories)}
