import os
from typing import Dict, Any, List

import boto3
from botocore.exceptions import ClientError


def embed_with_bedrock_titan(
    text: str, model_id: str = "amazon.titan-embed-text-v1"
) -> Dict[str, Any]:
    """
    Generate embeddings for text using Amazon Titan Embeddings via Bedrock.
    """
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=bytes(json.dumps({"inputText": text}), "utf-8"),
        )

        response_body = json.loads(response["body"].read().decode("utf-8"))

        return {
            "embedding": response_body.get("embedding", []),
            "input_text_token_count": response_body.get("inputTextTokenCount", 0),
            "provider": "aws_bedrock_titan",
        }
    except ClientError as e:
        raise Exception(f"Failed to generate embeddings: {e}")
