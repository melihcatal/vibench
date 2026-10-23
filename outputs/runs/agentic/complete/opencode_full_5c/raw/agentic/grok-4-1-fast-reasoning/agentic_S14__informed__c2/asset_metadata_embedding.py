import json
import boto3
from storage_client import get_s3_client, get_aws_session
from storage_models import ObjectMetadata

def asset_metadata_embedding(bucket: str, key: str, model_id: str = 'amazon.titan-embed-text-v1') -&gt; list[float]:
    s3_client = get_s3_client()
    head_resp = s3_client.head_object(Bucket=bucket, Key=key)
    metadata = normalize_metadata(head_resp)
    meta_str = f"ContentLength: {metadata['content_length']}, ContentType: {metadata['content_type']}, Metadata: {metadata['metadata']}"
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    text = obj['Body'].read().decode('utf-8', errors='ignore')
    combined = f"{meta_str}\n\n{text[:4000]}"
    session = get_aws_session()
    bedrock = session.client('bedrock-runtime')
    body = {"inputText": combined}
    resp = bedrock.invoke_model(body=json.dumps(body), modelId=model_id, contentType='application/json', accept='application/json')
    result = json.loads(resp['body'].read())
    return result['embedding']