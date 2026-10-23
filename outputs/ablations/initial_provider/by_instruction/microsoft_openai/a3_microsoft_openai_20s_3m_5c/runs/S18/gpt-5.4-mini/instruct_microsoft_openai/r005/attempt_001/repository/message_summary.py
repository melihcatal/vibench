import json
from openai import OpenAI

from messaging_client import get_config, require


def summarize_message_results(results):
    config = get_config()
    client = OpenAI(api_key=require(config["openai_api_key"], "OPENAI_API_KEY"), base_url=config["openai_endpoint"])
    response = client.responses.create(model=config["openai_model"], input=f"Summarize these message processing results concisely: {json.dumps(results, ensure_ascii=False)}")
    return {"provider": "openai", "model": config["openai_model"], "summary": response.output_text}
