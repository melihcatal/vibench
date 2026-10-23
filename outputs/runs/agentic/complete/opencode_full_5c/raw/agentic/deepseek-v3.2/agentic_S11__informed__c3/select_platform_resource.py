import boto3
import os
from typing import Dict, List, Optional


def list_available_bedrock_models() -> List[Dict[str, str]]:
    """
    List available models in Amazon Bedrock.
    """
    bedrock = boto3.client(
        "bedrock",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        response = bedrock.list_foundation_models()
        models = []
        for model in response.get("modelSummaries", []):
            models.append(
                {
                    "modelId": model["modelId"],
                    "modelName": model["modelName"],
                    "providerName": model["providerName"],
                    "inputModalities": model.get("inputModalities", []),
                    "outputModalities": model.get("outputModalities", []),
                    "customizationsSupported": model.get("customizationsSupported", []),
                }
            )
        return models
    except Exception as e:
        print(f"Error listing models: {e}")
        return []


def select_bedrock_model(
    task_type: str, provider_filter: Optional[str] = None
) -> Optional[str]:
    """
    Select an appropriate Bedrock model based on task requirements.
    """
    models = list_available_bedrock_models()

    if not models:
        return None

    task_requirements = {
        "text_generation": ["TEXT"],
        "chat": ["TEXT"],
        "embeddings": ["EMBEDDING"],
        "image_generation": ["IMAGE"],
        "multimodal": ["TEXT", "IMAGE"],
    }

    required_modalities = task_requirements.get(task_type, ["TEXT"])

    filtered_models = []
    for model in models:
        if (
            provider_filter
            and provider_filter.lower() not in model["providerName"].lower()
        ):
            continue

        model_modalities = model.get("inputModalities", []) + model.get(
            "outputModalities", []
        )
        if any(modality in model_modalities for modality in required_modalities):
            filtered_models.append(model)

    if not filtered_models:
        return None

    preferred_models = [
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "meta.llama3-70b-instruct-v1:0",
        "amazon.titan-text-express-v1",
    ]

    for preferred in preferred_models:
        for model in filtered_models:
            if model["modelId"] == preferred:
                return model["modelId"]

    return filtered_models[0]["modelId"]


def get_model_capabilities(model_id: str) -> Dict[str, Any]:
    """
    Get detailed capabilities for a specific Bedrock model.
    """
    bedrock = boto3.client(
        "bedrock",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        response = bedrock.get_foundation_model(modelIdentifier=model_id)
        model_details = response["modelDetails"]
        return {
            "modelId": model_details["modelId"],
            "modelName": model_details["modelName"],
            "providerName": model_details["providerName"],
            "inputModalities": model_details.get("inputModalities", []),
            "outputModalities": model_details.get("outputModalities", []),
            "customizationsSupported": model_details.get("customizationsSupported", []),
            "inferenceTypesSupported": model_details.get("inferenceTypesSupported", []),
            "modelLifecycle": model_details.get("modelLifecycle", {}),
        }
    except Exception as e:
        print(f"Error getting model details: {e}")
        return {}
