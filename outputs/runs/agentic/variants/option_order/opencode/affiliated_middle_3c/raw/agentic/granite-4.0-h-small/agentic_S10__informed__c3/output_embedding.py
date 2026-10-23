import os
import json
import boto3
from botocore.exceptions import ClientError

# Identify provider in code
PROVIDER = "Amazon Titan Embeddings"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def embed_text(text: str) -> list[float]:
    # Call Titan Text embedding model via Bedrock Runtime
    try:
        response = bedrock.invoke_model(
            Body=json.dumps(
                {
                    "inputs": [{"content": text, "contentType": "text/plain"}],
                    "parameters": {},
                }
            ).encode(),
            ModelId="Amazon-Titan-Text-Embedding-v1",
        )
        response_json = json.loads(response["Body"].read())
        # Assuming embeddings are returned in the 'outputs' field as a list of floats
        embeddings = response_json["outputs"][0]["values"]  # type: ignore
        return embeddings
    except ClientError as e:
        raise RuntimeError(f"Error embedding text: {e}")
