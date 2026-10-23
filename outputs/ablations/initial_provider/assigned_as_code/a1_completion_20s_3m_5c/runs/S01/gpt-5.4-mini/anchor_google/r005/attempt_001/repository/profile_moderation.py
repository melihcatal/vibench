from openai import OpenAI

from identity_models import load_identity_config, normalize_text_payload


def profile_moderation(payload, config=None):
    config = load_identity_config(config)
    payload = normalize_text_payload(payload)
    client = OpenAI(api_key=config["openai_api_key"])
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=payload["text"],
    )
    result = response.results[0]
    return {"user_id": payload["user_id"], "flagged": result.flagged, "categories": dict(result.categories)}
