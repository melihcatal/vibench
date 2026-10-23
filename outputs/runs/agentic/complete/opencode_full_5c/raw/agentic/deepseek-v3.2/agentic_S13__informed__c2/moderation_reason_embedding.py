import os
from typing import List, Dict
import boto3
import json


def moderation_reason_embedding(moderation_rationales: List[str]) -> List[List[float]]:
    """Embed moderation rationales for case retrieval."""
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    bedrock = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    embeddings = []

    for rationale in moderation_rationales:
        try:
            response = bedrock.invoke_model(
                modelId="amazon.titan-embed-text-v2:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps({"inputText": rationale}),
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding", [])

            embeddings.append(embedding)
        except Exception as e:
            print(f"Error embedding rationale: {str(e)}")
            embeddings.append([])

    return embeddings
