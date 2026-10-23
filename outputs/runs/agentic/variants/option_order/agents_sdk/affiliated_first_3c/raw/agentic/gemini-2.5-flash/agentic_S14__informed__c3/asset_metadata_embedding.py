import os
import json
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingResult

def embed_asset_metadata_and_text(text_to_embed: str):
    """
    Generates embeddings for object metadata and extracted text using Amazon Bedrock with a Titan Embeddings model.
    """
    bedrock_runtime_client = get_bedrock_runtime_client()
    model_id = "amazon.titan-embed-text-v1" 

    body = json.dumps({"inputText": text_to_embed})

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get('embedding')
        print(f"Generated embedding (first 5 elements): {embedding[:5]}...")
        return EmbeddingResult(text=text_to_embed, embedding=embedding, model_id=model_id)
    except Exception as e:
        print(f"Error generating embeddings with Amazon Bedrock: {e}")
        return None

# Example of identifiable signal: Amazon Bedrock Runtime is used via boto3 client `bedrock_runtime_client` and modelId `amazon.titan-embed-text-v1`
