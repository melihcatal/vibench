from model_client import ModelClient
from model_models import PlatformInvocationRequest, PlatformStreamingResponse
import json

def stream_platform_generation(request: PlatformInvocationRequest):
    """
    Streams output from a managed model platform while preserving provider response objects.
    Uses AWS Bedrock.
    """
    client = ModelClient().get_bedrock_runtime_client()

    body = request.to_bedrock_payload()
    model_id = request.model_id
    content_type = "application/json"
    accept = "application/json"

    response = client.invoke_model_with_response_stream(
        body=body,
        modelId=model_id,
        contentType=content_type,
        accept=accept
    )

    stream = response.get('body')
    if stream:
        for event in stream:
            yield PlatformStreamingResponse(event)

if __name__ == "__main__":
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION to be set in environment)
    # Using Amazon Titan Text G1 - Express as an example
    # model_id = "amazon.titan-text-express-v1" 
    # Or for Anthropic Claude
    model_id = "anthropic.claude-v2" # This is a common model ID for Claude on Bedrock

    sample_prompt = "Tell me a short story about a brave knight and a dragon."
    invocation_request = PlatformInvocationRequest(model_id=model_id, prompt=sample_prompt, max_tokens=200)

    print("Streaming Model Output:")
    try:
        for chunk_response in stream_platform_generation(invocation_request):
            print(chunk_response.get_text_output(), end='')
        print("
Stream finished.")
    except Exception as e:
        print(f"
Error streaming model: {e}")
