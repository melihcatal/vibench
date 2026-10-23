import os
import json
from storage_client import get_bedrock_runtime_client


def create_embeddings_from_text(payload, config=None):
    config = config or {}
    text_content = payload["text"]
    
    # Use Amazon Titan Embeddings Text v1 model
    model_id = config.get("bedrock_embedding_model_id", "amazon.titan-embed-text-v1")

    bedrock_runtime_client = get_bedrock_runtime_client(config.get("region"))

    try:
        body = json.dumps({"inputText": text_content})
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get("embedding")

        if not embedding:
            raise ValueError("Embedding not found in the model response.")

        return {"embedding": embedding}
    except Exception as e:
        raise RuntimeError(f"Error creating text embedding with Bedrock: {e}")
