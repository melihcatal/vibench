from openai import OpenAI

from messaging_client import get_config, require


def check_message_safety(payload_text):
    config = get_config()
    client = OpenAI(api_key=require(config["openai_api_key"], "OPENAI_API_KEY"), base_url=config["openai_endpoint"])
    response = client.moderations.create(model="omni-moderation-latest", input=str(payload_text))
    result = response.results[0]
    return {"provider": "openai", "model": "omni-moderation-latest", "flagged": bool(result.flagged), "categories": dict(result.categories)}
