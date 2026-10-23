import boto3
import os

def select_bedrock_model_resource(model_id: str | None = None) -> list[dict] | dict:
    """
    Resolves a provider-specific model resource from AWS Bedrock.

    Args:
        model_id (str, optional): The ID of a specific model to describe. If None, lists all available models.

    Returns:
        list[dict] | dict: A list of available models or details of a specific model.
    """
    client = boto3.client(
        "bedrock",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    if model_id:
        response = client.get_foundation_model(modelIdentifier=model_id)
        return response.get("modelDetails", {})
    else:
        response = client.list_foundation_models()
        return response.get("modelSummaries", [])
