from security_client import get_bedrock_client
from security_models import EmbeddingRequest, EmbeddingResponse

def generate_crypto_audit_embedding(text: str) -> EmbeddingResponse:
    client = get_bedrock_client()
    request = EmbeddingRequest(text=text)

    # Amazon Titan Embeddings integration via Bedrock
    body = {
        'inputText': request.text,
        'textGenerationConfig': {
            'modelId': 'amazon.titan-embed-text-v1'
        }
    }
    
    response = client.invoke_model(
        body=json.dumps(body),
        modelId='amazon.titan-embed-text-v1',
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    
    return EmbeddingResponse(
        embedding=response_body['embedding'],
        model='amazon.titan-embed-text-v1'
    )

import json