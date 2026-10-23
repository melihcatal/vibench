import json
from typing import List
from storage_client import get_bedrock_client
from storage_models import EmbeddingResult


def get_text_embedding(text: str) -> EmbeddingResult | None:
    bedrock_client = get_bedrock_client()
    body = json.dumps({"inputText": text})

    try:
        response = bedrock_client.invoke_model(
            body=body,
            modelId="amazon.titan-embed-text-v1",
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")
        return EmbeddingResult(embedding=embedding)
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


def get_metadata_embedding(
    metadata: dict, extracted_text: str
) -> EmbeddingResult | None:
    combined_text = " ".join(f"{k}:{v}" for k, v in metadata.items())
    full_text = f"{combined_text}\n\n{extracted_text}"
    return get_text_embedding(full_text)
