from model_client import get_bedrock_runtime_client


def localized_platform_output(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(config)
    target_locale = config.get("locale", "es")
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": f"Translate the following text to {target_locale}: {payload.get('text', '')}"}]}],
    )
    text = "".join(block.get("text", "") for block in response.get("output", {}).get("message", {}).get("content", []) if "text" in block)
    return {"text": text, "locale": target_locale, "response": response}
