from model_client import bedrock_runtime, invoke_json_model, load_model_config
from model_models import extract_text


def result_translate(text: str, target_language: str) -> str:
    config = load_model_config("anthropic.claude-3-haiku-20240307-v1:0")
    client = bedrock_runtime(config.region)
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.1,
        "messages": [{"role": "user", "content": f"Translate the following into {target_language}:\n\n{text}"}],
    }
    raw = invoke_json_model(client, config.model_id, payload)
    return extract_text(raw).strip()
