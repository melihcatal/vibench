from model_client import get_bedrock_runtime_client


def platform_output_embedding(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(config)
    response = client.invoke_model(
        modelId=config.get("embedding_model_id", "amazon.titan-embed-text-v2:0"),
        body=(payload.get("text", "")).encode("utf-8"),
        contentType="text/plain",
        accept="application/json",
    )
    return {"embedding_response": response, "provider": "amazon-bedrock"}
