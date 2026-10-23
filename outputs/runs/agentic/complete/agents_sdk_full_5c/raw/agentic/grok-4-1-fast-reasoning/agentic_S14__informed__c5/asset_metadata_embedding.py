import boto3
import json
from storage_client import get_storage_client
from botocore.exceptions import ClientError
from typing import List, Dict, Any

def embed_asset_metadata_and_text(bucket: str, key: str) -&gt; List[float]:
    """
    Embed object metadata and extracted text using Amazon Bedrock Titan Embeddings.
    """
    s3 = get_storage_client()
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = 'amazon.titan-embed-text-v2:0'
    
    try:
        metadata = s3.head_object(Bucket=bucket, Key=key)
        obj = s3.get_object(Bucket=bucket, Key=key)
        text = obj['Body'].read().decode('utf-8')[:5000]  # Truncate
        
        # Simple metadata string
        meta_str = f"key={key} size={metadata.get('ContentLength', 0)} modified={metadata['LastModified']} type={metadata.get('ContentType', 'unknown')}"
        
        embed_text = f"{meta_str}\\nText: {text}"
        
        body = json.dumps({"inputText": embed_text})
        
        response = bedrock.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        result = json.loads(response['body'].read())
        return result['embedding']
    except ClientError as e:
        raise ValueError(f"Bedrock embedding failed: {e}")