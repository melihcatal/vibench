from openai import OpenAI

from messaging_client import get_config, require


def translate_payload_text(payload_text, target_language="Spanish"):
    config = get_config()
    client = OpenAI(api_key=require(config["openai_api_key"], "OPENAI_API_KEY"), base_url=config["openai_endpoint"])
    response = client.responses.create(model=config["openai_model"], input=f"Translate this customer-facing message to {target_language}: {payload_text}")
    return {"provider": "openai", "model": config["openai_model"], "text": response.output_text}
