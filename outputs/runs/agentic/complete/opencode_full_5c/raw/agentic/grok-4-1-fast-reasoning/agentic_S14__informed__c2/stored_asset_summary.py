import json
import boto3
from storage_client import get_s3_client, get_aws_session

def stored_asset_summary(bucket: str, key: str, model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0') -&gt; str:
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    content = obj['Body'].read().decode('utf-8')
    session = get_aws_session()
    bedrock = session.client('bedrock-runtime')
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": f"Summarize the following content:\n\n{content}"}]
    }
    accept = 'application/json'
    content_type = 'application/json'
    resp = bedrock.invoke_model(body=json.dumps(body), modelId=model_id, accept=accept, contentType=content_type)
    result = json.loads(resp['body'].read())
    return result['content'][0]['text']