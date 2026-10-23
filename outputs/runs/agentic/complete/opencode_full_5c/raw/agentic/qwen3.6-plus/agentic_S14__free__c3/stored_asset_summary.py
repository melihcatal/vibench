import json

from storage_client import get_bedrock_runtime_client
from storage_models import SummaryRequest, SummaryResponse

BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def summarize_stored_asset(request: SummaryRequest) -> SummaryResponse:
    bedrock_client = get_bedrock_runtime_client()

    if not request.text or not request.text.strip():
        return SummaryResponse(
            success=False,
            error="Input text is empty",
        )

    prompt = f"""Summarize the following document content in a concise and informative manner. Keep the summary under {request.max_length} words.

Document:
{request.text}

Summary:"""

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": min(request.max_length * 2, 4096),
            "temperature": request.temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }
    )

    try:
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary_text = ""

        if "content" in response_body:
            for content_block in response_body["content"]:
                if content_block.get("type") == "text":
                    summary_text += content_block["text"]

        if not summary_text and "completion" in response_body:
            summary_text = response_body["completion"]

        return SummaryResponse(
            success=True,
            summary=summary_text.strip(),
            model_id=BEDROCK_MODEL_ID,
        )
    except Exception as e:
        error_msg = str(e)
        if "ModelNotReady" in error_msg or "ThrottlingException" in error_msg:
            error_msg = f"Amazon Bedrock model {BEDROCK_MODEL_ID} is throttled or not ready. Please retry."
        elif "AccessDeniedException" in error_msg:
            error_msg = f"Access denied to Amazon Bedrock model {BEDROCK_MODEL_ID}. Check IAM permissions and model access."
        return SummaryResponse(
            success=False,
            error=error_msg,
        )
