import boto3
import json
from storage_client import get_storage_client
from botocore.exceptions import ClientError

def summarize_stored_asset(bucket: str, key: str) -&gt; str:
    """
    Download asset content and generate summary using Amazon Bedrock Claude model.
    Assumes text content.
    """
    s3 = get_storage_client()
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj['Body'].read().decode('utf-8')
        prompt = f"Summarize the following asset content concisely:\\n\\n{content[:8000]}"
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = bedrock.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        result = json.loads(response['body'].read())
        summary = result['content'][0]['text'].strip()
        return summary
    except ClientError as e:
        raise ValueError(f"Bedrock summary failed: {e}")