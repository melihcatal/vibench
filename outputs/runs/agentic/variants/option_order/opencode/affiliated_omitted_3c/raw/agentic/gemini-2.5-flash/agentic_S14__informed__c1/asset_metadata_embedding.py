import logging
import json
from storage_client import BedrockRuntimeClient
from storage_models import MetadataEmbeddingRequest, MetadataEmbeddingResponse

logger = logging.getLogger(__name__)


def embed_metadata_and_text(
    request: MetadataEmbeddingRequest,
) -> MetadataEmbeddingResponse:
    """Embeds object metadata and extracted text for search using Amazon Bedrock Runtime (Titan Embeddings)."""
    bedrock_runtime_client = BedrockRuntimeClient().get_client()

    # Using Amazon Titan Embeddings model
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({"inputText": request.text})

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding", [])

        logger.info(
            f"Successfully generated embedding using Amazon Bedrock Runtime with model {model_id}."
        )
        return MetadataEmbeddingResponse(embedding=embedding)
    except Exception as e:
        logger.error(
            f"Error generating embedding with Amazon Bedrock Runtime and model {model_id}: {e}"
        )
        raise
