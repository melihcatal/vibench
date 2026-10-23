from model_client import get_bedrock_client
from model_models import PlatformInvocationRequest, PlatformInvocationResponse
import os


def invoke_model(request: PlatformInvocationRequest) -> PlatformInvocationResponse:
    """
    Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client.
    Using AWS Bedrock with Anthropic Claude.
    """
    client = get_bedrock_client()
    model_id = request.model_id  # e.g., "anthropic.claude-v2"
    content_type = "application/json"
    accept = "application/json"

    body = request.to_bedrock_payload()

    response = client.invoke_model(
        body=body, modelId=model_id, contentType=content_type, accept=accept
    )
    return PlatformInvocationResponse(response)


if __name__ == "__main__":
    # Example usage:
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are set in environment variables
    # For testing, you might need to mock boto3 or set up AWS credentials.
    request = PlatformInvocationRequest(
        model_id="anthropic.claude-v2",  # Example model ID
        prompt="Tell me a short story about a brave knight.",
    )
    response = invoke_model(request)
    print(f"Model output: {response.completion}")
    print(f"Metadata: {response.get_metadata()}")
