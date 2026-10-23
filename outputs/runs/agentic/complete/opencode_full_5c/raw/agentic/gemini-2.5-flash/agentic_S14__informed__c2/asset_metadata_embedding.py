import json
from storage_client import get_bedrock_runtime_client
from storage_models import EmbedMetadataRequest, EmbedMetadataResponse


def embed_metadata_text(request: EmbedMetadataRequest) -> EmbedMetadataResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        # Using Amazon Titan Embeddings G1 - Text
        model_id = "amazon.titan-embed-text-v1"

        body = json.dumps({"inputText": request.text})

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")

        if not embedding:
            raise ValueError("Embedding not found in the response.")

        return EmbedMetadataResponse(embedding=embedding)
    except Exception as e:
        raise RuntimeError(f"Failed to generate embedding using Bedrock: {e}")
