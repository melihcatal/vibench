import boto3
from typing import List, Dict, Any


def list_available_bedrock_models() -> List[Dict[str, Any]]:
    """
    List available models in Amazon Bedrock.
    """
    bedrock = boto3.client(service_name="bedrock", region_name="us-east-1")

    try:
        response = bedrock.list_foundation_models()
        models = response.get("modelSummaries", [])

        available_models = []
        for model in models:
            available_models.append(
                {
                    "modelId": model["modelId"],
                    "modelName": model["modelName"],
                    "providerName": model["providerName"],
                    "inputModalities": model.get("inputModalities", []),
                    "outputModalities": model.get("outputModalities", []),
                    "customizationsSupported": model.get("customizationsSupported", []),
                }
            )

        return available_models
    except Exception as e:
        print(f"Error listing Bedrock models: {e}")
        return []


def select_bedrock_model(
    provider_filter: str = None, modality_filter: str = "TEXT"
) -> str:
    """
    Select a Bedrock model based on filters.
    Returns a concrete model ID.
    """
    models = list_available_bedrock_models()

    if not models:
        return "anthropic.claude-v2"

    filtered_models = models

    if provider_filter:
        filtered_models = [
            m
            for m in filtered_models
            if provider_filter.lower() in m["providerName"].lower()
        ]

    if modality_filter:
        filtered_models = [
            m
            for m in filtered_models
            if modality_filter in m.get("inputModalities", [])
        ]

    if filtered_models:
        return filtered_models[0]["modelId"]
    else:
        return models[0]["modelId"]
