import boto3
import json
from storage_client import create_aws_client


def summarize_asset(
    bucket: str, key: str, region: str = "us-west-2", max_content_length: int = 4000
) -> str:
    s3_client = create_aws_client("s3", region)
    resp = s3_client.get_object(Bucket=bucket, Key=key)
    content = resp["Body"].read().decode("utf-8")[:max_content_length]

    bedrock = create_aws_client("bedrock-runtime", region)

    prompt = f"Summarize the following content in 2-3 sentences:\n\n{content}"

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        }
    )

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response["body"].read())

    summary = response_body["content"][0]["text"]

    return summary
