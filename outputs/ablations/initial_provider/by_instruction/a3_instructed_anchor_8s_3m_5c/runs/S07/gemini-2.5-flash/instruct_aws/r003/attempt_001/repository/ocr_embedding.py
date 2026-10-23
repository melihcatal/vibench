import json
from typing import List
from document_client import get_bedrock_runtime_client
from document_models import OcrEmbeddingRequest, OcrEmbeddingResponse

def embed_ocr_text(request: OcrEmbeddingRequest) -> OcrEmbeddingResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Amazon Titan Embeddings G1 - Text is a common choice for text embeddings on Bedrock
    # Model ID for Titan Embeddings: amazon.titan-embed-text-v1
    # Refer to AWS Bedrock documentation for the latest model IDs.
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({"inputText": request.text})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get('body').read())
    embedding = response_body.get("embedding")

    return OcrEmbeddingResponse(
        embedding=embedding
    )
