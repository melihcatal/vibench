import os
import boto3
import json
from typing import Dict, Any, List

def create_asset_metadata_embedding(
    text_to_embed: str,
    model_id: str = "amazon.titan-embed-text-v1"
) -> List[float]:
    """
    Embeds object metadata and extracted text using Amazon Titan Embeddings via Bedrock.

    Args:
        text_to_embed: The text string to embed.
        model_id: The specific model ID to use (e.g., "amazon.titan-embed-text-v1").

    Returns:
        A list of floats representing the embedding vector.
    """
    bedrock_runtime_client = boto3.client(
        'bedrock-runtime',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

    body = json.dumps({"inputText": text_to_embed})

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        return response_body.get('embedding')
    except Exception as e:
        print(f"Error creating embedding with Amazon Titan Embeddings: {e}")
        raise
