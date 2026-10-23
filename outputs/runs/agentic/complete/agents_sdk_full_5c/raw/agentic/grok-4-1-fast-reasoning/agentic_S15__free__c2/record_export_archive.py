import os
import boto3
import json
from typing import List, Dict, Any

s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION', 'us-east-1'))

def archive_documents(documents: List[Dict[str, Any]], bucket_name: str, prefix: str) -> List[str]:
    keys = []
    for i, doc in enumerate(documents):
        key = f"{prefix}/archive/doc_{i}.json"
        body = json.dumps(doc, indent=2).encode('utf-8')
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=body,
            ContentType='application/json'
        )
        keys.append(key)
    return keys