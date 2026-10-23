import json
from embeddings_client import get_bedrock_client

def embed_text(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using AWS Bedrock.
    """
    bedrock_runtime = get_bedrock_client()
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({"inputText": text})
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return embedding
