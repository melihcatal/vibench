import boto3
import json
from storage_client import create_aws_client


def create_asset_embedding(
    bucket: str, key: str, region: str = "us-west-2", max_text_length: int = 8000
) -> list[float]:
    s3_client = create_aws_client("s3", region)

    meta_resp = s3_client.head_object(Bucket=bucket, Key=key)
    metadata_str = json.dumps(dict(meta_resp.get("Metadata", {})))

    content_resp = s3_client.get_object(Bucket=bucket, Key=key)
    text = content_resp["Body"].read().decode("utf-8")[:max_text_length]

    input_text = f"Metadata: {metadata_str}\\n\\nContent: {text}"

    bedrock = create_aws_client("bedrock-runtime", region)

    body = json.dumps({"inputText": input_text})

    model_id = "amazon.titan-embed-text-v1"

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response["body"].read())

    return response_body["embedding"]
