import json
from model_client import get_bedrock_runtime_client
from model_models import BedrockInvokeRequest, BedrockInvokeResponse

def invoke_claude_with_metadata(request: BedrockInvokeRequest) -> BedrockInvokeResponse:
    """
    Invokes a model on Amazon Bedrock and returns the output along with
    platform metadata.
    """
    bedrock_runtime = get_bedrock_runtime_client()
    
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

    # Extract platform metadata from the top-level response
    platform_metadata = response.get('ResponseMetadata', {})
    
    # Extract model-specific usage metadata from the response body
    response_body = json.loads(response.get('body').read())
    completion = response_body['content'][0]['text']
    usage_metadata = response_body.get('usage', {})

    full_metadata = {
        'requestId': platform_metadata.get('RequestId'),
        'httpStatusCode': platform_metadata.get('HTTPStatusCode'),
        'headers': platform_metadata.get('HTTPHeaders'),
        'input_tokens': usage_metadata.get('input_tokens'),
        'output_tokens': usage_metadata.get('output_tokens'),
        'model_id': request.model_id,
    }

    return BedrockInvokeResponse(text=completion, metadata=full_metadata)
