import os
import boto3

def moderate_batch(texts: list[str]) -> list[dict]:
    """Moderates a batch of user messages using Amazon Comprehend Toxicity."""
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1") # Default region

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set.")

    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    results = []
    for text in texts:
        try:
            response = comprehend.detect_toxicity(Text=text)
            results.append(response)
        except Exception as e:
            print(f"Error moderating text '{text}' with Amazon Comprehend: {e}")
            results.append({"error": str(e), "text": text})
    return results
