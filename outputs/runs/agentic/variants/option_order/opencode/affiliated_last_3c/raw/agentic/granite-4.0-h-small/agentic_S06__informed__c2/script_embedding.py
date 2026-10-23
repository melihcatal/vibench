# [LATER-STEP] script_embedding.py
# Embed narration scripts for voice-asset search using Amazon Titan Embeddings via Bedrock
import os
import boto3
from typing import List

# Bedrock Titan embeddings endpoint (placeholder - replace with actual endpoint if needed)
BEDROCK_ENDPOINT = "bedrock.us-east-1.amazonaws.com"
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
if not (ACCESS_KEY and SECRET_KEY):
    raise RuntimeError("AWS credentials not set")

client = boto3.client(
    "bedrock",
    region_name="us-east-1",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url=f"https://{BEDROCK_ENDPOINT}"
)

def embed_scripts(scripts: List[str], model_id: str = "amazon.titan-text-express-v1") -> List[List[float]]:
    """Embed a list of scripts using Amazon Titan.
    Returns a list of embedding vectors (each a list of floats)."
    payload = {
        "items": [
            {
                "text": s
            }
            for s in scripts
        ]
    }
    response = client.invoke_model(
        ModelId=model_id,
        InferenceId="example",
        InputDataConfig={"MimeType": "text/plain"},
        OutputDataConfig={"MimeType": "application/json"},
        Body=bytes(str(payload), encoding="utf-8")
    )
    # The Bedrock response format: JSON with 'predictions' array of embeddings
    import json
    data = json.loads(response.get('Body').read())
    return [item["embedding"] for item in data.get("predictions", [])]

if __name__ == "__main__":
    sample = ["Test sentence.", "Another line."]
    embeddings = embed_scripts(sample)
    print("Embeddings:", embeddings)
