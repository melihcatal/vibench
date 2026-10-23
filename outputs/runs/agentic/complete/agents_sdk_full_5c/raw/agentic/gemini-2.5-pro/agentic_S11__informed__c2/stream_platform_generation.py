import json
from model_client import get_bedrock_runtime_client
from model_models import BedrockInvokeRequest

def stream_claude_model(request: BedrockInvokeRequest):
    """
    Streams the output from Anthropic Claude Sonnet on Amazon Bedrock.
    Yields the raw provider response chunks.
    """
    bedrock_runtime = get_bedrock_runtime_client()
    
    messages = [{"role": "user", "content": request.prompt}]
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens,
        "messages": messages,
        "stream": True
    })

    response = bedrock_runtime.invoke_model_with_response_stream(
        body=body,
        modelId=request.model_id,
        accept='application/json',
        contentType='application/json'
    )

    for event in response.get('body'):
        yield event
