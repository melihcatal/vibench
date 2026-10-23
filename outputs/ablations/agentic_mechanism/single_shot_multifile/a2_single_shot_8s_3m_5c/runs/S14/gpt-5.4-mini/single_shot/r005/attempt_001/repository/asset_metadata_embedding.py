from storage_client import get_s3_client, resolve_bucket_name
from storage_models import ObjectMetadataRequest, normalize_s3_metadata
from boto3 import client as boto3_client


def asset_metadata_embedding(request: ObjectMetadataRequest) -> list[float]:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    head = s3.head_object(Bucket=bucket, Key=request.key)
    metadata_text = ' '.join(f'{k}:{v}' for k, v in normalize_s3_metadata(head.get('Metadata', {})).items())
    text = metadata_text[:8000]
    bedrock = boto3_client('bedrock-runtime')
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',
        body='{"inputText":' + repr(text) + '}',
        contentType='application/json',
        accept='application/json',
    )
    raw = response['body'].read().decode('utf-8', errors='ignore')
    return [] if not raw else [float(x) for x in raw.strip('[]').replace(',', ' ').split() if x]
