import json
from storage_client import get_bedrock_runtime_client
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse


def summarize_stored_asset_content(
    request: StoredAssetSummaryRequest,
) -> StoredAssetSummaryResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()
    prompt = f"""Human: Summarize the following text:

<text>
{request.text_content}
</text>

Assistant:"""
    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": request.max_tokens,
            "temperature": 0.1,
            "top_p": 0.9,
        }
    )
    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId="anthropic.claude-v2",  # Using Anthropic Claude for summarization via Bedrock
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response.get("body").read())
    summary = response_body.get("completion")
    return StoredAssetSummaryResponse(summary=summary.strip())
