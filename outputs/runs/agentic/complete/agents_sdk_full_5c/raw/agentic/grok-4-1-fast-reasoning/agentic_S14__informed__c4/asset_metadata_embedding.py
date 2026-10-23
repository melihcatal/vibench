import boto3
import json
from typing import List, Dict, Any

def asset_metadata_embedding(
    bucket: str,
    key: str,
    extracted_text: str
) -> List[float]:
    s3_client = boto3.client('s3')
    metadata_str = '{}'
    try:
        meta_response = s3_client.head_object(Bucket=bucket, Key=key)
        metadata_str = json.dumps({k: str(v) for k, v in meta_response.items() if k != 'ResponseMetadata'})
    except Exception:
        pass
    
    text_to_embed = extracted_text + ' Metadata: ' + metadata_str
    
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
    body = json.dumps({
        "inputText": text_to_embed
    })
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=body,
        contentType="application/json",
        accept="application/json"
    )
    response_body = json.loads(response.get('body').read())
    return response_body['embedding']