from model_client import get_bedrock_runtime_client
from model_models import extract_text_from_response, normalize_messages


def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(config)
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=normalize_messages(payload),
    )
    text = extract_text_from_response(response)
    metadata = {
        "usage": response.get("usage"),
        "request_id": response.get("ResponseMetadata", {}).get("RequestId"),
        "model_id": config.get("model_id", "us.amazon.nova-pro-v1:0"),
    }
    return {"text": text, "metadata": metadata}
