import os
import json
import boto3
from storage_client import get_bedrock_runtime_client
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse

def summarize_stored_asset(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Using AWS Bedrock with Anthropic Claude for summarization
    # modelId: anthropic.claude-v2, anthropic.claude-instant-v1, anthropic.claude-3-sonnet-20240229-v1:0, etc.
    # We'll use anthropic.claude-v2 for this example.
    model_id = "anthropic.claude-v2"
    
    prompt = f"Human: Summarize the following text in a concise manner, focusing on key information:\n\n{request.text}\n\nAssistant:"
    
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": request.max_tokens,
        "temperature": 0.1,
        "top_p": 0.9
    })

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get('body').read())
    summary_text = response_body.get('completion', '').strip()

    return StoredAssetSummaryResponse(summary=summary_text)
