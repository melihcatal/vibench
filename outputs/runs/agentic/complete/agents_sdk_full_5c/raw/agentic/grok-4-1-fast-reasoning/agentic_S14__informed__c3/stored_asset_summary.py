import boto3
import json

def stored_asset_summary(bucket: str, key: str) -> str:
    """
    Summarizes content extracted from a stored asset using Anthropic Claude via Amazon Bedrock.
    Assumes UTF-8 text file.
    """
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    
    bedrock_client = boto3.client('bedrock-runtime')
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    prompt = f"Please provide a concise summary of the following content:\n\n{content}"
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}]
    })
    
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        contentType='application/json',
        accept='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    summary = response_body['content'][0]['text']
    return summary.strip()