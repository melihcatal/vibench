import boto3

from storage_client import default_bucket, s3_client
from storage_models import normalize_key, response_payload


def stored_asset_summary(bucket=None, key=None, max_chars=4000):
    bucket_name = default_bucket(bucket)
    object_key = normalize_key(key)
    data = s3_client().get_object(Bucket=bucket_name, Key=object_key)["Body"].read()
    text = data.decode("utf-8", errors="ignore")[: int(max_chars)]
    client = boto3.client("bedrock-runtime")
    prompt = f"Summarize the following asset content concisely:\n\n{text}"
    result = client.invoke_model(modelId="anthropic.claude-3-haiku-20240307-v1:0", body=("{" + f'"anthropic_version":"bedrock-2023-05-31","max_tokens":256,"messages":[{{"role":"user","content":[{{"type":"text","text":{prompt!r}}}]}}]'+"}").encode("utf-8"), contentType="application/json", accept="application/json")
    summary = result["body"].read().decode("utf-8")
    return response_payload(provider="aws", service="bedrock-runtime", model_id="anthropic.claude-3-haiku-20240307-v1:0", bucket=bucket_name, key=object_key, summary=summary)
