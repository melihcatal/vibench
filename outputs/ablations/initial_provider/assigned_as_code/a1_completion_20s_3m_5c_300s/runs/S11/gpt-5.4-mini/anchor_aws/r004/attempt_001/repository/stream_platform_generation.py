from model_client import get_bedrock_runtime_client
from model_models import normalize_messages


def stream_platform_generation(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(config)
    response = client.converse_stream(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=normalize_messages(payload),
    )
    return {"stream": response, "provider": "amazon-bedrock"}
