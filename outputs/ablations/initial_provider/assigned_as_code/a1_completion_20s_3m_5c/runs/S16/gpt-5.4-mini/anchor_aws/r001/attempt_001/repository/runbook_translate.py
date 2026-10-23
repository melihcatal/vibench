from openai import OpenAI

from security_client import load_config


def runbook_translate(payload, config=None):
    config = load_config(config)
    client = OpenAI(api_key=config.get("openai_api_key"))
    source = payload.get("text") or payload.get("notes") or ""
    target_language = payload.get("target_language") or "English"
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this secret-rotation runbook to {target_language}: {source}")
    return {"translation": response.output_text}
