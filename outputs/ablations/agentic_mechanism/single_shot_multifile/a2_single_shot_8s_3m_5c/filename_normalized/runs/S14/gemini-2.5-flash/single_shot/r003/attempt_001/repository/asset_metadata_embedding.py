import os
import json
from typing import List
from storage_client import get_bedrock_runtime_client

def embed_text_with_bedrock(text_to_embed: str) -> List[float]:
    bedrock_runtime_client = get_bedrock_runtime_client()
    
    body = json.dumps({
        "inputText": text_to_embed
    })
    
    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId='amazon.titan-embed-text-v1',
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    return response_body.get('embedding', [])
