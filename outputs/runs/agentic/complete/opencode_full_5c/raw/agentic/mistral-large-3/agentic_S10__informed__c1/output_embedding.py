import boto3
from typing import List


def embed_output(
    text: str, model_id: str = "amazon.titan-embed-text-v1"
) -> List[float]:
    """
    Embed model outputs for clustering or retrieval using Amazon Titan Embeddings via Bedrock.
    """
    client = boto3.client("bedrock-runtime")

    response = client.invoke_model(
        modelId=model_id, body=json.dumps({"inputText": text})
    )

    result = json.loads(response["body"].read().decode("utf-8"))
    return result["embedding"]
