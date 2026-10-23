import boto3
import json
from model_client import BedrockClient
from model_models import ModelInvocationRequest, ModelInvocationResponse

def invoke_bedrock_model(request: ModelInvocationRequest) -> ModelInvocationResponse:
    """
    Invokes a provider-managed model (AWS Bedrock) through a platform client.
    """
    client = BedrockClient().get_client()
    
    body = json.dumps({
        "prompt": request.prompt,
        "max_tokens_to_sample": request.max_tokens,
        "temperature": request.temperature
    })
    
    response = client.invoke_model(
        body=body,
        modelId=request.model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get('body').read())
    
    return ModelInvocationResponse(
        generated_text=response_body.get('completion'),
        model_id=request.model_id
    )
