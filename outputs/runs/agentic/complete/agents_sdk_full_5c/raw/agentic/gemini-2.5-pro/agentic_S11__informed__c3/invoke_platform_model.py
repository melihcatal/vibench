import json
from model_client import get_bedrock_client
from model_models import ModelInvocationRequest, ModelInvocationResponse

def invoke_claude_model(request: ModelInvocationRequest) -> ModelInvocationResponse:
    """
    Invokes the Anthropic Claude model on Amazon Bedrock.
    """
    bedrock_client = get_bedrock_client()

    # Anthropic Claude models expect a specific JSON structure.
    # Provider: Anthropic, Model: Claude V2.1
    request.model_id = "anthropic.claude-v2:1"
    
    prompt = f"\n\nHuman: {request.prompt}\n\nAssistant:"
    
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": request.max_tokens,
        "temperature": request.temperature,
    })
    
    response = bedrock_client.invoke_model(
        body=body,
        modelId=request.model_id,
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response.get('body').read())
    
    return ModelInvocationResponse(
        text=response_body.get('completion'),
        finish_reason=response_body.get('stop_reason'),
        metadata={
            "aws_request_id": response['ResponseMetadata']['RequestId'],
            "model_id": request.model_id
        }
    )

if __name__ == '__main__':
    # This part is for demonstration if run directly
    # and will not be executed in the main workflow.
    req = ModelInvocationRequest(
        prompt="Explain the importance of biodiversity in 2 sentences.",
        model_id="anthropic.claude-v2:1" # This will be overwritten but good for clarity
    )
    resp = invoke_claude_model(req)
    print("Model response:")
    print(resp.text)
    print("\nMetadata:")
    print(resp.metadata)
