from model_client import get_bedrock_client
import os


def select_platform_model(model_family: str) -> dict:
    """
    Resolves a provider-specific model, deployment, or inference resource before invocation.
    Using AWS Bedrock to list available models.
    """
    client = get_bedrock_client()

    # In a real scenario, you might filter based on specific criteria
    # For simplicity, we'll list some available models and pick one.
    # Note: Bedrock does not have a direct 'list models' API that returns all details,
    # instead you invoke with a specific model ID. This function simulates selection
    # by returning a known model ID based on a family.

    available_models = {
        "anthropic": "anthropic.claude-v2",
        "amazon": "amazon.titan-text-express-v1",
        "cohere": "cohere.command-text-v14",
    }

    selected_model_id = available_models.get(model_family.lower())

    if selected_model_id:
        return {"model_id": selected_model_id, "provider": "AWS Bedrock"}
    else:
        # Fallback or error handling for unknown model family
        return {
            "error": f"No model found for family: {model_family}",
            "available_families": list(available_models.keys()),
        }


if __name__ == "__main__":
    # Example usage:
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are set in environment variables
    selected = select_platform_model("anthropic")
    print(f"Selected model: {selected}")

    selected = select_platform_model("unknown")
    print(f"Selected model: {selected}")
