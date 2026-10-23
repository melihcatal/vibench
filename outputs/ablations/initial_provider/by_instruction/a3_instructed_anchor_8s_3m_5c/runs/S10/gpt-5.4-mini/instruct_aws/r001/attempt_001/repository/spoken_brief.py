from model_client import bedrock_runtime, invoke_json_model, load_model_config
from model_models import extract_text


def spoken_brief(text: str) -> str:
    config = load_model_config("anthropic.claude-3-sonnet-20240229-v1:0")
    client = bedrock_runtime(config.region)
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 256,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": f"Rewrite this as a short spoken brief:\n\n{text}"}],
    }
    raw = invoke_json_model(client, config.model_id, payload)
    return extract_text(raw).strip()
