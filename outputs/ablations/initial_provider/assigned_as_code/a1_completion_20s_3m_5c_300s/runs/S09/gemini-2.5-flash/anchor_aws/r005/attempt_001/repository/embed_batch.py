import json
import boto3
from embeddings_client import BedrockEmbeddingsClient
from embeddings_models import prepare_bedrock_payload, parse_bedrock_response

def embed_batch(texts, config=None):
    config = config or {}
    bedrock_client_wrapper = BedrockEmbeddingsClient(region_name=config.get("region"))
    client = bedrock_client_wrapper.get_client()
    model_id = bedrock_client_wrapper.get_model_id()

    embeddings = []
    for text in texts:
        payload = prepare_bedrock_payload(text)
        response = client.invoke_model(modelId=model_id,
            body=payload, contentType="application/json", accept="application/json")
        embedding = parse_bedrock_response(response["body"])
        embeddings.append(embedding)
    return {"embeddings": embeddings}
