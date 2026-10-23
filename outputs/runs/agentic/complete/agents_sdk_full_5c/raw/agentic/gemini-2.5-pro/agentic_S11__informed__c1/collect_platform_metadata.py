import json
from model_client import get_bedrock_runtime_client
from model_models import InvokeRequest, InvokeResponse, ModelMetadata

def invoke_model_with_metadata(model_id: str, request: InvokeRequest) -> InvokeResponse:
    """
    Invokes a Bedrock model and returns the output along with platform metadata.
    """
    bedrock_runtime = get_bedrock_runtime_client()
    
    body = {
        "prompt": f"\n\nHuman: {request.prompt}\n\nAssistant:",
        "max_tokens_to_sample": request.max_tokens
    }

    response = bedrock_runtime.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response["body"].read())
    completion = response_body.get("completion", "")

    # Extract metadata from response headers
    headers = response.get("ResponseMetadata", {}).get("HTTPHeaders", {})
    metadata = ModelMetadata(
        input_token_count=int(headers.get("x-amzn-bedrock-input-token-count", 0)),
        output_token_count=int(headers.get("x-amzn-bedrock-output-token-count", 0)),
        request_id=response.get("ResponseMetadata", {}).get("RequestId"),
        model_id=model_id
    )

    return InvokeResponse(text=completion, metadata=metadata)
