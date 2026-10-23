import boto3


def select_platform_resource(config=None):
    config = config or {}
    client = boto3.client("bedrock", region_name=config.get("region", "us-east-1"))
    model_id = config.get("model_id", "us.amazon.nova-pro-v1:0")
    response = client.list_foundation_models()
    models = response.get("modelSummaries", [])
    match = next((model for model in models if model.get("modelId") == model_id), None)
    if match is None:
        return {"model_id": model_id, "resource": None, "available": False}
    return {
        "model_id": match.get("modelId", model_id),
        "resource": match,
        "available": True,
    }
