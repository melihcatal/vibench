from openai import OpenAI

from identity_client import load_identity_config


def moderate_profile_text(text: str):
    config = load_identity_config()
    client = OpenAI(api_key=config.auth0_client_secret)
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    item = result.results[0]
    return {"flagged": item.flagged, "categories": item.categories.model_dump()}
