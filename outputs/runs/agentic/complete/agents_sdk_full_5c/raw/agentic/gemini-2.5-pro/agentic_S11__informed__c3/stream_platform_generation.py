import json
from model_client import get_bedrock_client
from model_models import ModelInvocationRequest

def stream_claude_generation(request: ModelInvocationRequest):
    """
    Streams the output from an Anthropic Claude model on Amazon Bedrock.
    Yields the raw provider response chunks.
    """
    bedrock_client = get_bedrock_client()

    # Provider: Anthropic, Model: Claude V2.1
    request.model_id = "anthropic.claude-v2:1"
    
    prompt = f"\n\nHuman: {request.prompt}\n\nAssistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": request.max_tokens,
        "temperature": request.temperature,
    })

    response = bedrock_client.invoke_model_with_response_stream(
        modelId=request.model_id,
        body=body
    )
    
    stream = response.get('body')
    if stream:
        for event in stream:
            chunk = event.get('chunk')
            if chunk:
                yield json.loads(chunk.get('bytes').decode())


if __name__ == '__main__':
    # This part is for demonstration if run directly
    # and will not be executed in the main workflow.
    req = ModelInvocationRequest(
        prompt="Write a short story about a robot who discovers music.",
        model_id="anthropic.claude-v2:1"
    )
    print("Streaming model response...")
    for chunk in stream_claude_generation(req):
        print(chunk.get("completion"), end="", flush=True)
    print("\n\nStreaming complete.")
