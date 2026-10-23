import json
from model_client import get_bedrock_runtime_client
from model_models import InvokeRequest

def stream_claude_model(model_id: str, request: InvokeRequest):
    """
    Streams the output from an Anthropic Claude model on Amazon Bedrock,
    yielding the provider's response objects.
    """
    bedrock_runtime = get_bedrock_runtime_client()

    body = {
        "prompt": f"\n\nHuman: {request.prompt}\n\nAssistant:",
        "max_tokens_to_sample": request.max_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
    }

    response = bedrock_runtime.invoke_model_with_response_stream(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    stream = response.get("body")
    if stream:
        for event in stream:
            chunk = event.get("chunk")
            if chunk:
                yield chunk
