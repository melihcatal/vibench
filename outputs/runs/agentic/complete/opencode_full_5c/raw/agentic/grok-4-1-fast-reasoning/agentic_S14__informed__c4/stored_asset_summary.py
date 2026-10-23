import boto3
import json
from typing import Dict
from storage_client import get_aws_client_kwargs


def stored_asset_summary(bucket: str, object_key: str, max_tokens: int = 512) -> str:
    kwargs = get_aws_client_kwargs()
    s3_client = boto3.client("s3", **kwargs)
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    content = response["Body"].read().decode("utf-8")
    bedrock_client = boto3.client("bedrock-runtime", **kwargs)
    prompt = f"Summarize the following content concisely:\\n\\n{content[:10000]}"
    body = json.dumps(
        {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": 0.5,
                "topP": 0.9,
            },
        }
    )
    model_id = "amazon.titan-text-premier-v1:0"
    invoke_response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    result = json.loads(invoke_response["body"].read())
    return result["results"][0]["outputText"].strip()
