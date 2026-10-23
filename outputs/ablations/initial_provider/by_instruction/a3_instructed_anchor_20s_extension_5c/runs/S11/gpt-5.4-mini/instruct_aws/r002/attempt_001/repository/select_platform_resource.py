import os
from model_client import bedrock_client


def select_platform_resource(preferred_model_id=None):
    client = bedrock_client()
    model_id = preferred_model_id or os.getenv("BEDROCK_MODEL_ID") or "anthropic.claude-3-sonnet-20240229-v1:0"
    inference_profile_arn = os.getenv("BEDROCK_INFERENCE_PROFILE_ARN")
    if inference_profile_arn:
        return {"inference_profile_arn": inference_profile_arn, "model_id": model_id}
    try:
        client.get_foundation_model(modelIdentifier=model_id)
    except Exception:
        pass
    return {"model_id": model_id}
