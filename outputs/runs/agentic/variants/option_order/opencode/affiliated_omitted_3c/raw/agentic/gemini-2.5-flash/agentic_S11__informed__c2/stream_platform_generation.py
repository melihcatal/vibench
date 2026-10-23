from model_client import get_bedrock_client
from model_models import PlatformInvocationRequest, PlatformStreamResponse
import os


def stream_model_generation(request: PlatformInvocationRequest):
    """
    Streams output from a managed model platform while preserving provider response objects.
    Using AWS Bedrock with Anthropic Claude for streaming.
    """
    client = get_bedrock_client()
    model_id = request.model_id  # e.g., "anthropic.claude-v2"
    content_type = "application/json"
    accept = "application/json"

    body = request.to_bedrock_payload()

    response = client.invoke_model_with_response_stream(
        body=body, modelId=model_id, contentType=content_type, accept=accept
    )

    event_stream = response.get("body")
    for event in event_stream:
        stream_response = PlatformStreamResponse(event)
        if stream_response.chunk:
            yield stream_response.chunk


if __name__ == "__main__":
    # Example usage:
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION are set in environment variables
    # For testing, you might need to mock boto3 or set up AWS credentials.
    request = PlatformInvocationRequest(
        model_id="anthropic.claude-v2",  # Example model ID
        prompt="Write a very short poem about the ocean.",
    )
    print("Streaming model output:")
    for chunk in stream_model_generation(request):
        print(chunk, end="", flush=True)
    print("\nStreaming complete.")
