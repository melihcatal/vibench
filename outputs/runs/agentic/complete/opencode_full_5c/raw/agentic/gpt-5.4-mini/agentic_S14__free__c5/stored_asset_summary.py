import os

import boto3

from storage_client import bucket_name, client


def stored_asset_summary(bucket: str | None, key: str):
    s3 = client()
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )
    body = (
        s3.get_object(Bucket=bucket_name(bucket), Key=key)["Body"]
        .read()
        .decode("utf-8", errors="ignore")
    )
    prompt = f"Summarize this asset in one concise paragraph:\n\n{body}"
    return bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=(
            "{"
            + f'"messages":[{{"role":"user","content":[{{"type":"text","text":{prompt!r}}}]}}],"max_tokens":200'
            + "}"
        ).encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
