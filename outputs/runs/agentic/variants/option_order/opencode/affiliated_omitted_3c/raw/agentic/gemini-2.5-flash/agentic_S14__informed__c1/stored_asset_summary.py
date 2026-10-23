import logging
import json
from storage_client import BedrockRuntimeClient
from storage_models import AssetSummaryRequest, AssetSummaryResponse

logger = logging.getLogger(__name__)


def summarize_asset_content(request: AssetSummaryRequest) -> AssetSummaryResponse:
    """Summarizes content extracted from a stored asset using Amazon Bedrock Runtime (Anthropic Claude Instant)."""
    bedrock_runtime_client = BedrockRuntimeClient().get_client()

    # Using Anthropic Claude Instant model
    model_id = "anthropic.claude-instant-v1"

    prompt = (
        f"Human: Summarize the following text:\n\n{request.text_content}\n\nAssistant:"
    )

    body = json.dumps({"prompt": prompt, "max_tokens_to_sample": request.max_tokens})

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary_text = response_body.get("completion", "").strip()

        logger.info(
            f"Successfully summarized asset content using Amazon Bedrock Runtime with model {model_id}."
        )
        return AssetSummaryResponse(summary_text=summary_text)
    except Exception as e:
        logger.error(
            f"Error summarizing asset content with Amazon Bedrock Runtime and model {model_id}: {e}"
        )
        raise
