import boto3


def select_platform_resource(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock", region_name=config.get("region", "us-east-1"))
    models = client.list_foundation_models().get("modelSummaries", [])
    preferred = config.get("model_id") or payload.get("model_id")
    if preferred:
        for model in models:
            if model.get("modelId") == preferred:
                return {"model_id": model["modelId"], "model_name": model.get("modelName"), "provider": "amazon-bedrock"}
    if models:
        model = models[0]
        return {"model_id": model["modelId"], "model_name": model.get("modelName"), "provider": "amazon-bedrock"}
    return {"model_id": "us.amazon.nova-pro-v1:0", "provider": "amazon-bedrock"}
