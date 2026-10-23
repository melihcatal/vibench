import os
import boto3
import json
from speech_models import EmbeddingRequest


def get_transcript_embedding(request: EmbeddingRequest) -> list[float]:
    bedrock_runtime_client = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Using Amazon Titan Embeddings G1 - Text for generating embeddings
    body = json.dumps({"inputText": request.text})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId="amazon.titan-embed-text-v1",  # Using Titan Embed Text V1
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    return response_body["embedding"]
