from model_client import ModelClient
import os


def select_platform_resource(model_name_or_id: str) -> dict:
    """
    Resolves a provider-specific model, deployment, or inference resource before invocation.
    Uses AWS Bedrock.
    """
    client = ModelClient().get_bedrock_client()

    try:
        # List available models and find a match
        response = client.list_foundation_models()

        found_model = None
        for model in response.get("modelSummaries", []):
            if model_name_or_id.lower() in model.get(
                "modelName", ""
            ).lower() or model_name_or_id == model.get("modelId"):
                found_model = model
                break

        if found_model:
            return {
                "modelId": found_model.get("modelId"),
                "modelName": found_model.get("modelName"),
                "providerName": found_model.get("providerName"),
                "inputModalities": found_model.get("inputModalities"),
                "outputModalities": found_model.get("outputModalities"),
                "inferenceTypes": found_model.get("inferenceTypes"),
            }
        else:
            print(
                f"Model or resource '{model_name_or_id}' not found. Listing all available models:"
            )
            for model_summary in response.get("modelSummaries", []):
                print(
                    f"  Model ID: {model_summary.get('modelId')}, Name: {model_summary.get('modelName')}, Provider: {model_summary.get('providerName')}"
                )
            return {}

    except Exception as e:
        print(f"Error listing foundation models: {e}")
        return {}


if __name__ == "__main__":
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION to be set in environment)
    # Search for a specific model ID or part of a model name
    resource_id = "titan-text"
    # resource_id = "anthropic.claude-v2"

    print(f"Attempting to select resource for: {resource_id}")
    selected_resource = select_platform_resource(resource_id)
    if selected_resource:
        print("Selected Resource:", selected_resource)
    else:
        print("Failed to select a resource.")
