import os
from typing import Optional
import boto3
from storage_client import get_storage_client

def summarize_stored_asset(
    object_key: str,
    output_object_key: Optional[str] = None
) -> str:
    """
    Summarizes content extracted from a stored asset in AWS S3 using AWS Bedrock.
    Returns the summary text.
    """
    s3_client = get_storage_client()
    bedrock_client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "default-bucket")
    output_key = output_object_key or f"summary-output/{object_key}.txt"

    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=object_key
    )
    text = response["Body"].read().decode("utf-8")

    body = {
        "inputText": f"Summarize the following text:\n\n{text}",
        "textGenerationConfig": {
            "maxTokenCount": 4096,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    bedrock_response = bedrock_client.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=bytes(str(body).encode("utf-8"))
    )

    response_body = bedrock_response["body"].read().decode("utf-8")
    summary = eval(response_body)["results"][0]["outputText"]

    s3_client.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=summary.encode("utf-8")
    )

    return summary