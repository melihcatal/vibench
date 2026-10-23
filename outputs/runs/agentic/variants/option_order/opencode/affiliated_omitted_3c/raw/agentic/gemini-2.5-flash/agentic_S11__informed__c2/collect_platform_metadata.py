from model_client import get_bedrock_client
from model_models import PlatformInvocationRequest, PlatformInvocationResponse
import os


def collect_model_output_with_metadata(request: PlatformInvocationRequest) -> dict:
    """
    Returns model output together with provider platform metadata such as usage, resource IDs, or model handles.
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
    platform_response = PlatformInvocationResponse(response)

    # AWS Bedrock metadata is primarily in the response headers and body
    metadata = platform_response.get_metadata()
    metadata["response_headers"] = response.get("ResponseMetadata", {}).get(
        "HTTPHeaders"
    )
    # For Bedrock, usage details are often within the body for certain models.
    # This example assumes Claude, where 'completion' is direct,
    # usage would require deeper parsing depending on the model.
    # For some models, Bedrock includes 'usage' in the JSON body.
    # For Claude, the prompt tokens and completion tokens are not directly in the invoke_model response metadata.
    # You would typically calculate them based on input/output, or use a higher-level SDK feature.
    # For demonstration, we'll just return what's easily available.

    return {"completion": platform_response.completion, "metadata": metadata}


if __name__ == "__main__":
    # Example usage:
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are set in environment variables
    request = PlatformInvocationRequest(
        model_id="anthropic.claude-v2",  # Example model ID
        prompt="What is the capital of France?",
    )
    result = collect_model_output_with_metadata(request)
    print(f"Completion: {result['completion']}")
    print(f"Metadata: {result['metadata']}")
