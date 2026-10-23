import json
import logging
from storage_client import get_bedrock_runtime_client
from storage_models import SummaryResult

logger = logging.getLogger(__name__)


def summarize_content(text_content: str, max_tokens: int = 500) -> SummaryResult:
    bedrock_runtime_client = get_bedrock_runtime_client()
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"  # Using Claude 3 Sonnet as a capable model

    prompt_template = """
    Human: Summarize the following text:

    <text>
    {text}
    </text>

    Assistant: Here is a concise summary of the text:
    """
    prompt = prompt_template.format(text=text_content)

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
        }
    )

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary = response_body["content"][0]["text"]
        return SummaryResult(summary_text=summary)
    except Exception as e:
        logger.error(
            f"Error summarizing content using Bedrock with model {model_id}: {e}"
        )
        raise
