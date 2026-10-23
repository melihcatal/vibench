import os
from typing import Dict, List

import boto3


def embed_asset_metadata_and_text(text: str, metadata: Dict[str, str]) -> List[float]:
    """
    Embed object metadata and extracted text using Amazon Titan Embeddings via Bedrock.
    """
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    input_text = f"Metadata: {metadata}\nText: {text}"

    body = {
        "inputText": input_text,
    }

    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=bytes(str(body).replace("'", '"'), "utf-8"),
    )

    response_body = eval(response["body"].read().decode())
    return response_body["embedding"]