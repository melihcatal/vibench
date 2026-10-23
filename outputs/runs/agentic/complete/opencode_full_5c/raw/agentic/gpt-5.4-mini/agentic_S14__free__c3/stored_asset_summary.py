import os

import boto3

from storage_client import get_s3_client


def stored_asset_summary(bucket: str, key: str):
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8", errors="ignore")
    bedrock = boto3.client(
        "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    prompt = (
        f"Summarize the following asset content in 5 bullet points:\n{text[:12000]}"
    )
    body = (
        '{"inputText": '
        + repr(prompt)
        + ', "textGenerationConfig": {"maxTokenCount": 300, "temperature": 0.2, "topP": 0.9}}'
    )
    return bedrock.invoke_model(modelId="amazon.titan-text-express-v1", body=body)
