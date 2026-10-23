from model_client import ModelClient
from model_models import PlatformInvocationRequest, PlatformInvocationResponse
import json


def invoke_platform_model(
    request: PlatformInvocationRequest,
) -> PlatformInvocationResponse:
    """
    Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client.
    Uses AWS Bedrock.
    """
    client = ModelClient().get_bedrock_runtime_client()

    body = request.to_bedrock_payload()
    model_id = request.model_id
    content_type = "application/json"
    accept = "application/json"

    response = client.invoke_model(
        body=body, modelId=model_id, contentType=content_type, accept=accept
    )

    response_body = json.loads(response["body"].read())

    # Provider-specific metadata can be extracted from the response object
    # For now, we'll include a simplified metadata structure.
    metadata = {"bedrock_response_metadata": response.get("ResponseMetadata", {})}

    return PlatformInvocationResponse(response_body, metadata)


if __name__ == "__main__":
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION to be set in environment)
    # Using Amazon Titan Text G1 - Express as an example
    # model_id = "amazon.titan-text-express-v1"
    # Or for Anthropic Claude
    model_id = "anthropic.claude-v2"  # This is a common model ID for Claude on Bedrock

    sample_prompt = "Hello, what is the capital of France?"
    invocation_request = PlatformInvocationRequest(
        model_id=model_id, prompt=sample_prompt, max_tokens=100
    )

    try:
        response = invoke_platform_model(invocation_request)
        print("Invoked Model Output:", response.get_text_output())
        print("Metadata:", response.get_metadata())
    except Exception as e:
        print(f"Error invoking model: {e}")
