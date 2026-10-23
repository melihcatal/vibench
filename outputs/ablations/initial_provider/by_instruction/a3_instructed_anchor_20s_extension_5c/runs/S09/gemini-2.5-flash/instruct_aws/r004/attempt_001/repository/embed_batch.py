import json
from embeddings_client import get_bedrock_client

def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a batch of text strings using AWS Bedrock.
    """
    bedrock_runtime = get_bedrock_client()
    model_id = "amazon.titan-embed-text-v1"

    # AWS Bedrock's Titan Text Embeddings model can take a batch of texts
    body = json.dumps({"inputText": texts})
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    # The response for a batch should be a list of embeddings
    embeddings = response_body.get("embeddings")

    return embeddings
