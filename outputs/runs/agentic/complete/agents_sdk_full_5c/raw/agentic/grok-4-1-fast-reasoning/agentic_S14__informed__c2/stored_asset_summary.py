import boto3
import json
from storage_client import get_s3_client, get_bucket_name

def stored_asset_summary(
    bucket_name: str | None = None,
    key: str,
    summary_prompt: str = "Provide a concise summary of the asset content:"
) -> str:
    if bucket_name is None:
        bucket_name = get_bucket_name()
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    content = obj["Body"].read().decode("utf-8")
    full_prompt = f"{summary_prompt}\n\n{content}"
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps({
        "prompt": full_prompt,
        "max_gen_len": 512,
        "temperature": 0.7,
        "top_p": 0.9
    })
    model_id = "meta.llama3-8b-instruct-v1:0"
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response["body"].read())
    return response_body["generation"]
