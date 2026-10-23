import json
from model_client import get_bedrock_runtime_client
from model_models import BedrockInvokeRequest, BedrockInvokeResponse

def invoke_claude_model(request: BedrockInvokeRequest) -> BedrockInvokeResponse:
    """
    Invokes the Anthropic Claude Sonnet model on Amazon Bedrock.
    """
    bedrock_runtime = get_bedrock_runtime_client()
    
    # Claude 3 Sonnet requires a specific JSON structure
    messages = [{"role": "user", "content": request.prompt}]
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens,
        "messages": messages
    })

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=request.model_id,
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())
    completion = response_body['content'][0]['text']
    
    return BedrockInvokeResponse(text=completion)
