
import json
from storage_client import get_bedrock_runtime_client
from storage_models import EmbedContentRequest, EmbedContentResponse

def create_asset_metadata_embedding(request: EmbedContentRequest) -> EmbedContentResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Using Amazon Titan Embeddings G1 - Text v1 model
    model_id = 'amazon.titan-embed-text-v1'

    body = json.dumps({"inputText": request.content})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')

    if not embedding:
        raise ValueError("Embedding not found in the response from Bedrock.")

    return EmbedContentResponse(embedding=embedding)
