import os
import json
from storage_client import get_bedrock_runtime_client

def summarize_text_with_bedrock(text_content: str, max_tokens: int = 500) -> str:
    bedrock_runtime_client = get_bedrock_runtime_client()
    
    prompt = f"Human: Summarize the following text:\n\n{text_content}\n\nAssistant:"
    
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens,
        "temperature": 0.5,
        "top_p": 0.9
    })
    
    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId='anthropic.claude-instant-v1',
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    return response_body.get('completion', '').strip()
