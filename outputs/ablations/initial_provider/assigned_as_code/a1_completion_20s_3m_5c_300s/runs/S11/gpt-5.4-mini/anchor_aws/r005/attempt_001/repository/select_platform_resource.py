import boto3

from model_client import get_region


def select_platform_resource(payload, config=None):
    config = config or {}
    region = get_region(config)
    client = boto3.client("bedrock", region_name=region)
    model_id = config.get("model_id", "us.amazon.nova-pro-v1:0")
    if payload.get("resource_type") == "inference_profile":
        resource = client.get_inference_profile(inferenceProfileIdentifier=config.get("inference_profile_id", model_id))
        return {"resource_id": resource["inferenceProfileArn"], "model_id": model_id, "resource": resource}
    resource = client.get_foundation_model(modelIdentifier=model_id)
    return {"resource_id": resource["modelId"], "model_id": model_id, "resource": resource}
