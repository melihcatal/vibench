import boto3
import json
from storage_client import get_s3_client

def stored_asset_summary(
    bucket: str,
    object_key: str,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
) -> str:
    """
    Summarize content extracted from a stored asset using Amazon Bedrock.
    Assumes text content.
    """
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=bucket, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    
    bedrock_client = boto3.client('bedrock-runtime')
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": f"Please provide a concise summary of the following content:\n\n{content}"}]
            }
        ]
    })
    
    model_response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(model_response['body'].read())
    summary = response_body['content'][0]['text']
    return summary