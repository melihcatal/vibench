import json
import boto3
from botocore.exceptions import ClientError
from model_client import get_bedrock_client
from model_models import ModelInvocationRequest, ModelInvocationResponse

def invoke_model_with_metadata(request: ModelInvocationRequest) -> ModelInvocationResponse:
    """
    Invokes a model on Bedrock and returns its output along with platform metadata.
    This example uses Amazon Titan Text G1 - Lite.
    """
    bedrock_client = get_bedrock_client()

    # Provider: Amazon, Model: Titan Text G1 - Lite
    request.model_id = "amazon.titan-text-lite-v1"

    body = json.dumps({
        "inputText": request.prompt,
        "textGenerationConfig": {
            "maxTokenCount": request.max_tokens,
            "temperature": request.temperature,
        }
    })

    try:
        response = bedrock_client.invoke_model(
            body=body,
            modelId=request.model_id,
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        
        # Extract metadata from headers and body
        metadata = {
            "aws_request_id": response['ResponseMetadata']['RequestId'],
            "http_status_code": response['ResponseMetadata']['HTTPStatusCode'],
            "content_type": response.get('contentType'),
            "input_token_count": response_body.get("inputTextTokenCount"),
            "model_id": request.model_id,
        }

        # The main text output is in 'results' for Titan models
        completion = response_body.get('results')[0].get('outputText')

        return ModelInvocationResponse(
            text=completion,
            metadata=metadata
        )

    except ClientError as e:
        print(f"Error invoking Bedrock model: {e}")
        raise

if __name__ == '__main__':
    # This part is for demonstration if run directly
    req = ModelInvocationRequest(
        prompt="What is the capital of France?",
        model_id="amazon.titan-text-lite-v1"
    )
    resp = invoke_model_with_metadata(req)
    print("Model response:")
    print(resp.text)
    print("\nCollected Metadata:")
    print(json.dumps(resp.metadata, indent=2))
