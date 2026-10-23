import boto3
import json
from storage_client import get_s3_client
from typing import List

def asset_metadata_embedding(
    bucket: str,
    object_key: str,
    model_id: str = "amazon.titan-embed-text-v2:0"
) -> List[float]:
    """
    Embed object metadata and extracted text for search using Amazon Bedrock Titan Embeddings.
    """
    s3_client = get_s3_client()
    
    # Get metadata
    head_response = s3_client.head_object(Bucket=bucket, Key=object_key)
    metadata_str = f"size:{head_response.get('ContentLength', 0)} content_type:{head_response.get('ContentType', '')}"
    if 'Metadata' in head_response:
        metadata_str += f" metadata:{head_response['Metadata']}"
    
    # Get content
    get_response = s3_client.get_object(Bucket=bucket, Key=object_key)
    text = get_response['Body'].read().decode('utf-8', errors='ignore')[:4000]  # limit length
    
    combined_text = f"{metadata_str} text:{text}"
    
    bedrock_client = boto3.client('bedrock-runtime')
    
    body = json.dumps({
        "inputText": combined_text
    })
    
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    embedding = response_body['embedding']
    return embedding