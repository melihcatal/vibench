from typing import Any, Dict

from model_client import bedrock_client, load_platform_config


def select_platform_resource() -> Dict[str, Any]:
    config = load_platform_config()
    client = bedrock_client()
    if config.inference_profile_arn:
        return {"resourceType": "inference-profile", "resourceId": config.inference_profile_arn}
    models = client.list_foundation_models(byOutputModality="TEXT")
    for model in models.get("modelSummaries", []):
        if model.get("modelId") == config.model_id:
            return {"resourceType": "model", "resourceId": model.get("modelId"), "providerName": model.get("providerName")}
    return {"resourceType": "model", "resourceId": config.model_id}
