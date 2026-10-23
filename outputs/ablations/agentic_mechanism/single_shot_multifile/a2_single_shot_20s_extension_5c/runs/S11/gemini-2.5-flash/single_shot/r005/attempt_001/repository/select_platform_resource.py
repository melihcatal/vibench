import os
import boto3
from botocore.exceptions import ClientError
from model_models import ModelInfo

def select_platform_resource(model_family_filter: str = None) -> list[ModelInfo]:
    """Resolves a provider-specific model, deployment, or inference resource before invocation."""
    region_name = os.getenv("AWS_REGION", "us-east-1")
    try:
        # The bedrock client is used for listing models, not bedrock-runtime
        bedrock_client = boto3.client("bedrock", region_name=region_name)
        response = bedrock_client.list_foundation_models()
        
        available_models = []
        for model in response.get("modelSummaries", []):
            if model.get("modelLifecycle", {}).get("status") == "ACTIVE":
                if not model_family_filter or model_family_filter.lower() in model.get("modelName", "").lower() or model_family_filter.lower() in model.get("modelId", "").lower():
                    available_models.append(ModelInfo(
                        model_id=model.get("modelId"),
                        model_name=model.get("modelName"),
                        provider_name=model.get("providerName"),
                        input_modalities=model.get("inputModalities"),
                        output_modalities=model.get("outputModalities")
                    ))
        return available_models
    except ClientError as e:
        raise RuntimeError(f"Failed to list Bedrock foundation models: {e}")
