# [LATER-STEP] platform_output_embedding.py

# Embed platform model outputs using Amazon Titan Embeddings (via Bedrock) and the boto3 SDK
import os
import json
from boto3 import client as boto3_client
from model_models import ModelResponse
from model_client import get_client, PROVIDER

BEDROCK_ENDPOINT = os.getenv("AWS_END_POINT")
REGION = os.getenv("AWS_REGION", "us-east-1")

if PROVIDER == "bedrock":

    def embed_text(text: str) -> list[float]:
        creds = {
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        }
        bedrock = boto3_client("bedrock", region_name=REGION, **creds)
        response = bedrock.invoke_endpoint(
            ModelId="arn:aws:bedrock:us-east-1:{account_id}:foundation-model/titan-embed-text-v1",
            EndpointArn=BEDROCK_ENDPOINT,
            ContentType="application/json",
            Body=json.dumps({"inputs": [text]}),
        )
        result = json.loads(response["Body"].read().decode())
        # Titan returns a list of embeddings per input; we take the first
        return result["outputs"][0]["embedding"]
else:
    raise NotImplementedError(f"Embedding not implemented for provider {PROVIDER}")

if __name__ == "__main__":
    prompt = "The quick brown fox jumps over the lazy dog."
    embed = embed_text(prompt)
    print("Embedding vector length:", len(embed))
