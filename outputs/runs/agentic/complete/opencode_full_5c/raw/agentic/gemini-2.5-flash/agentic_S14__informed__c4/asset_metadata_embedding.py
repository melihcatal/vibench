import json
import logging
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingResult

logger = logging.getLogger(__name__)


def embed_text(text: str) -> EmbeddingResult:
    bedrock_runtime_client = get_bedrock_runtime_client()
    model_id = "amazon.titan-embed-text-v1"  # Titan Embeddings model

    body = json.dumps({"inputText": text})

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body["embedding"]
        return EmbeddingResult(embedding=embedding)
    except Exception as e:
        logger.error(
            f"Error generating embedding for text using Bedrock with model {model_id}: {e}"
        )
        raise
