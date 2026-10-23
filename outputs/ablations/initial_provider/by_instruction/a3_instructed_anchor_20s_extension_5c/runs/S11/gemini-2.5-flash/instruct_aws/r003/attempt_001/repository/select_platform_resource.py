import boto3
import os

def select_bedrock_model(model_family: str = "anthropic") -> str:
    client = boto3.client(
        "bedrock",
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    available_models = client.list_foundation_models(
        byProvider=model_family
    )
    # For simplicity, pick the first available model that is active and supports text generation
    for model in available_models.get("modelSummaries", []):
        if model.get("modelLifecycle", {}).get("status") == "ACTIVE" and \
           "TEXT" in model.get("outputModalities", []) and \
           "TEXT" in model.get("inputModalities", []):
            return model.get("modelId")
    raise ValueError(f"No active text generation model found for provider {model_family}")

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION environment variable or it will default to us-east-1
    # export AWS_REGION="your-aws-region"
    # export AWS_ACCESS_KEY_ID="your-access-key"
    # AWS_SECRET_ACCESS_KEY="your-secret-key"
    try:
        model_id = select_bedrock_model("anthropic")
        print(f"Selected Bedrock model ID: {model_id}")
    except ValueError as e:
        print(e)
