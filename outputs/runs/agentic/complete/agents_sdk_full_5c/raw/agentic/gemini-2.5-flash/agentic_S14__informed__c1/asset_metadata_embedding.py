import boto3
import json
import os

def get_text_embedding_with_bedrock(text: str):
    """
    Generates an embedding for text using Amazon Titan Embeddings via Bedrock.
    """
    bedrock_runtime_client = boto3.client('bedrock-runtime')
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({"inputText": text})

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get('embedding')
        print(f"Generated embedding for text (first 5 dimensions): {embedding[:5]}...")
        return embedding
    except Exception as e:
        print(f"Error generating text embedding with Bedrock: {e}")
        return None

