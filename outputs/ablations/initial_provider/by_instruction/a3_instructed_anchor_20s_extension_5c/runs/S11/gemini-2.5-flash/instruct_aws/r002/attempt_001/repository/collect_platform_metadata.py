import boto3
import json
from model_client import BedrockClient
from model_models import ModelInvocationRequest, ModelMetadataResponse

def collect_bedrock_metadata(request: ModelInvocationRequest) -> ModelMetadataResponse:
    """
    Returns model output together with provider platform metadata (AWS Bedrock).
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

    # Extract metadata. The exact metadata available depends on the model and the response structure.
    # For Bedrock, we might get things like input/output token counts, though this varies by model.
    # For a simple example, we'll include the model ID and a dummy usage count.
    metadata = {
        "model_id": request.model_id,
        "amazon_request_id": response['ResponseMetadata']['RequestId'] if 'ResponseMetadata' in response else 'N/A',
        # In a real scenario, usage would be parsed from response_body if available
        "usage": {"input_tokens": None, "output_tokens": None} # Placeholder
    }

    return ModelMetadataResponse(
        generated_text=response_body.get('completion'),
        metadata=metadata
    )
