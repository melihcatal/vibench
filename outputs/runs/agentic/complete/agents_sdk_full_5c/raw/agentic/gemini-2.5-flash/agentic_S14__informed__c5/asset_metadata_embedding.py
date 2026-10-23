import os
import json
from typing import List
from storage_client import get_bedrock_runtime_client

def embed_asset_metadata_and_text(text_to_embed: str) -> List[float] | None:
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        # Using Amazon Titan Embeddings G1 - Text v1
        # Model ID: amazon.titan-embed-text-v1
        model_id = "amazon.titan-embed-text-v1"

        body = json.dumps({"inputText": text_to_embed})

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        embedding = response_body.get('embedding')
        print(f"Text embedded using Amazon Titan Embeddings G1 - Text v1 successfully.")
        return embedding
    except Exception as e:
        print(f"Error generating embeddings with Amazon Bedrock: {e}")
        return None
