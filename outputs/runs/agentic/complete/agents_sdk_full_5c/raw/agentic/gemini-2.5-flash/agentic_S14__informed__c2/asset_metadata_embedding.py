import boto3
import json
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingRequest

def create_embeddings_for_asset_metadata(request: EmbeddingRequest) -> list[float]:
    bedrock_runtime = get_bedrock_runtime_client()
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({"inputText": request.text})

    try:
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get('body').read())
        return response_body['embedding']

    except bedrock_runtime.exceptions.ClientError as e:
        raise RuntimeError(f"Amazon Bedrock failed to create embeddings: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during embedding: {e}")
