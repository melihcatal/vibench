from model_client import bedrock_runtime, invoke_json_model, load_model_config


def prompt_safety(text: str) -> dict:
    config = load_model_config("anthropic.claude-3-haiku-20240307-v1:0")
    client = bedrock_runtime(config.region)
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 128,
        "temperature": 0.0,
        "messages": [{"role": "user", "content": f"Assess this text for unsafe content and return JSON with fields safe and reasons:\n\n{text}"}],
    }
    return invoke_json_model(client, config.model_id, payload)
