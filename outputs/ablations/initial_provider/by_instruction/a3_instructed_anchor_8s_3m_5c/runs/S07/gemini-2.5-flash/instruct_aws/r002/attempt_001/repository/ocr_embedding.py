import json
from document_client import get_bedrock_runtime_client
from document_models import EmbeddingResult

def embed_document_section(text: str) -> EmbeddingResult:
    bedrock_runtime_client = get_bedrock_runtime_client()
    
    model_id = "amazon.titan-embed-text-v1"
    accept = "application/json"
    content_type = "application/json"

    body = json.dumps({"inputText": text})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')

    return EmbeddingResult(embedding=embedding)
