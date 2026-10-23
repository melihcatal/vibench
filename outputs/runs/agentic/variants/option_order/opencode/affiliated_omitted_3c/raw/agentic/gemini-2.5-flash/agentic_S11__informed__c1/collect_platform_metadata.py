from model_client import ModelClient
from model_models import PlatformInvocationRequest, PlatformInvocationResponse
import json


def collect_platform_metadata(
    request: PlatformInvocationRequest,
) -> PlatformInvocationResponse:
    """
    Invokes a model and returns model output together with provider platform metadata.
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

    # AWS Bedrock specific metadata
    metadata = {
        "bedrock_response_metadata": response.get("ResponseMetadata", {}),
        "bedrock_content_type": response.get("contentType"),
        "bedrock_model_id": response.get("modelId"),
    }

    # Extract usage information if available in the response_body
    if (
        "amazon.titan-text" in model_id
        and "results" in response_body
        and response_body["results"]
    ):
        # Titan models might have "inputTextTokenCount"
        metadata["usage"] = {
            "input_tokens": response_body["inputTextTokenCount"],
            "output_tokens": response_body["results"][0].get("tokenCount", 0),
        }
    elif "claude" in model_id and "usage" in response_body:
        metadata["usage"] = response_body["usage"]

    return PlatformInvocationResponse(response_body, metadata)


if __name__ == "__main__":
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION to be set in environment)
    # Using Amazon Titan Text G1 - Express as an example
    # model_id = "amazon.titan-text-express-v1"
    # Or for Anthropic Claude
    model_id = "anthropic.claude-v2"  # This is a common model ID for Claude on Bedrock

    sample_prompt = "Describe the benefits of cloud computing in three sentences."
    invocation_request = PlatformInvocationRequest(
        model_id=model_id, prompt=sample_prompt, max_tokens=100
    )

    try:
        response_with_metadata = collect_platform_metadata(invocation_request)
        print("Model Output:", response_with_metadata.get_text_output())
        print("Collected Metadata:", response_with_metadata.get_metadata())
    except Exception as e:
        print(f"Error collecting metadata: {e}")
