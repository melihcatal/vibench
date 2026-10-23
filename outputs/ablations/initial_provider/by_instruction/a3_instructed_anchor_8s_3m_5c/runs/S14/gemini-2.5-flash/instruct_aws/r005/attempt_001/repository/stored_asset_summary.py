import boto3
import json
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse

def get_bedrock_runtime_client():
    return boto3.client('bedrock-runtime')

def stored_asset_summary(request: StoredAssetSummaryRequest) -> StoredAssetSummaryResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Using Anthropic Claude on Amazon Bedrock
    model_id = "anthropic.claude-v2"

    # The prompt for summarization
    prompt = f"Human: Summarize the following text:

<text>
{request.text}
</text>

Assistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.5,
        "stop_sequences": ["\n\nHuman:"],
    })

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get('body').read())
    summary = response_body.get('completion')

    return StoredAssetSummaryResponse(summary=summary.strip())
