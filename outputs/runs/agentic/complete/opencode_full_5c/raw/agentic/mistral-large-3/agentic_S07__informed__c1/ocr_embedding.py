import os
from typing import Dict, List
import boto3


def embed_document_sections(sections: List[str]) -> List[List[float]]:
    """
    Embeds extracted document sections using Amazon Titan Embeddings via Bedrock Runtime.
    """
    client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-west-2"),
    )

    embeddings = []
    model_id = "amazon.titan-embed-text-v1"

    for section in sections:
        response = client.invoke_model(modelId=model_id, body=section.encode("utf-8"))
        response_body = response.get("body").read().decode("utf-8")
        embedding = eval(response_body).get("embedding", [])
        embeddings.append(embedding)

    return embeddings
