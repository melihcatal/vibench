from embeddings_client import get_bedrock_client, TITAN_EMBED_TEXT_MODEL_ID
from embeddings_models import create_titan_embedding_request_body, parse_titan_embedding_response

def embed_text(text: str) -> list[float]:
    bedrock_runtime = get_bedrock_client()
    
    body = create_titan_embedding_request_body(text)
    
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=TITAN_EMBED_TEXT_MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = response['body'].read()
    embedding = parse_titan_embedding_response(response_body)
    
    return embedding
