import json
from model_models import ModelInvocationResponse
from typing import Dict
# Use Amazon Titan Embeddings via Bedrock runtime as the concrete embedding service.
import boto3
from botocore.exceptions import ClientError

def platform_output_embedding(raw_response: ModelInvocationResponse) -> Dict[str, Any]:
    """
    Embed the textual output using Amazon Titan Text Embeddings (Bedrock).
    Returns a dict with the original text and the embedding vector.
    """
    # Bedrock client
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    # Titan model ID for embeddings
    titan_model = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
    payload = {
        "inputs": [
            {
                "text": raw_response.text
            }
        ],
        "outputContentType": "application/json"
    }
    try:
        response = bedrock.embed_content(
            modelId=titan_model,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )
        # Response shape: { "embeddings": [{"index":0, "embedding":[...]}] }
        embeddings = response.get("embeddings", [])
        if not embeddings:
            raise ValueError("No embeddings returned")
        vec = embeddings[0]["embedding"]  # list of floats
        return {
            "text": raw_response.text,
            "embedding": vec,
            "embedding_service": "amazon.titan-embed-text-v1",
            "status": "ok"
        }
    except ClientError as e:
        return {
            "text": raw_response.text,
            "embedding": None,
            "status": "error",
            "error_message": str(e)
        }

# Simple CLI for testing
if __name__ == "__main__":
    deployment = os.getenv("DEPLOYMENT_ID")
    if not deployment:
        raise RuntimeError("DEPLOYMENT_ID must be set.")
    prompt = "Explain the principle of vector similarity in few words."
    response = collect_platform_metadata(deployment, prompt)
    embedding_result = platform_output_embedding(response)
    print(json.dumps(embedding_result, indent=2))
