from storage_client import get_bedrock_runtime_client
from storage_models import AssetSummaryRequest, AssetSummaryResponse
import json


def summarize_stored_asset(request: AssetSummaryRequest) -> AssetSummaryResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Construct the prompt using the provided template and text content
    prompt = request.prompt_template.format(text_content=request.text_content)

    # For Anthropic Claude models on Bedrock
    if request.model_id.startswith("anthropic.claude"):
        body = json.dumps(
            {
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 1024,
                "temperature": 0.7,
                "top_p": 1,
            }
        )
        model_id = (
            request.model_id
        )  # e.g., "anthropic.claude-v2", "anthropic.claude-instant-v1"
    else:
        # Default to a generic structure or raise an error for unsupported models
        raise ValueError(f"Unsupported model ID for summarization: {request.model_id}")

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())

    if request.model_id.startswith("anthropic.claude"):
        summary = response_body.get("completion")
    else:
        summary = "Summary not available for this model response structure."

    return AssetSummaryResponse(summary=summary, raw_response=response_body)
