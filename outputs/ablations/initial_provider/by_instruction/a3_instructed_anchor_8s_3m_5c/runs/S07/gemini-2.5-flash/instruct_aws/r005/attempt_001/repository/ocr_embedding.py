from document_client import DocumentClient
from document_models import EmbeddingRequest, EmbeddingResponse
import logging
import json

logger = logging.getLogger(__name__)

def create_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    client = DocumentClient()
    bedrock_runtime_client = client.bedrock_runtime_client

    embeddings_list = []
    for text_segment in request.text_segments:
        body = json.dumps({"inputText": text_segment})
        model_id = "amazon.titan-embed-text-v1"
        content_type = "application/json"
        accept = "*/*"

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            contentType=content_type,
            accept=accept
        )

        response_body = json.loads(response.get('body').read())
        embeddings_list.append(response_body.get('embedding'))

    return EmbeddingResponse(embeddings=embeddings_list)
