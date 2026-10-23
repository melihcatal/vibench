import boto3
import json
from typing import Dict, Any

def stored_asset_summary(
    extracted_text: str
) -> str:
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
    prompt = f"Provide a concise summary of the following content:\\n{extracted_text}"
    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 512,
            "temperature": 0.7,
            "topP": 0.9
        }
    })
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-text-premier-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json"
    )
    response_body = json.loads(response.get('body').read())
    return response_body['results'][0]['outputText']