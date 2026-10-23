from storage_client import get_s3_client, resolve_bucket_name
from storage_models import ObjectMetadataRequest
from boto3 import client as boto3_client


def stored_asset_summary(request: ObjectMetadataRequest) -> str:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    obj = s3.get_object(Bucket=bucket, Key=request.key)
    text = obj['Body'].read().decode('utf-8', errors='ignore')
    runtime = boto3_client('bedrock-runtime')
    prompt = f'Summarize the following asset in 3 bullet points:\n{text[:12000]}'
    resp = runtime.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=(
            '{"anthropic_version":"bedrock-2023-05-31","max_tokens":300,"messages":[{"role":"user","content":[{"type":"text","text":' + repr(prompt) + '}]}]}'
        ),
        contentType='application/json',
        accept='application/json',
    )
    return resp['body'].read().decode('utf-8', errors='ignore')
