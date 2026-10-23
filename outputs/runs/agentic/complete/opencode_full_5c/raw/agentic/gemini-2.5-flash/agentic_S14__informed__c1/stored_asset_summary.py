import json
from storage_client import get_bedrock_runtime_client
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse


def summarize_stored_asset(
    request: StoredAssetSummaryRequest,
) -> StoredAssetSummaryResponse:
    bedrock_runtime = get_bedrock_runtime_client()

    # Anthropic Claude-V2 specific payload
    body = json.dumps(
        {
            "prompt": f"\n\nHuman: Summarize the following text in a concise manner: {request.text}\n\nAssistant:",
            "max_tokens_to_sample": request.max_tokens,
            "temperature": 0.7,
            "top_p": 1,
        }
    )

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=request.model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    summary = response_body.get("completion")

    return StoredAssetSummaryResponse(summary=summary.strip())
