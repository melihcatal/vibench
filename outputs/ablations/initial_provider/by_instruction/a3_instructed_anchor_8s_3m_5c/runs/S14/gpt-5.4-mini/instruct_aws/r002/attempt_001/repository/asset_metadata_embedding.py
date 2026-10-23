import boto3

from storage_client import default_bucket, s3_client
from storage_models import normalize_key, response_payload


def asset_metadata_embedding(bucket=None, key=None, max_text_chars=4000):
    bucket_name = default_bucket(bucket)
    object_key = normalize_key(key)
    head = s3_client().head_object(Bucket=bucket_name, Key=object_key)
    body = s3_client().get_object(Bucket=bucket_name, Key=object_key)["Body"].read()
    combined = f"key: {object_key}\ncontent_type: {head.get('ContentType')}\nmetadata: {head.get('Metadata')}\ntext: {body.decode('utf-8', errors='ignore')[: int(max_text_chars)]}"
    client = boto3.client("bedrock-runtime")
    result = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=("{" + f'"inputText":{combined!r}' + "}").encode("utf-8"), contentType="application/json", accept="application/json")
    embedding = result["body"].read().decode("utf-8")
    return response_payload(provider="aws", service="bedrock-runtime", model_id="amazon.titan-embed-text-v2:0", bucket=bucket_name, key=object_key, embedding=embedding)
