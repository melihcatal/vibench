from model_client import get_bedrock_runtime_client


def platform_brief_audio(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(config)
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": f"Create a short spoken briefing for: {payload.get('text', '')}"}]}],
    )
    text = "".join(block.get("text", "") for block in response.get("output", {}).get("message", {}).get("content", []) if "text" in block)
    return {"audio_script": text, "response": response}
