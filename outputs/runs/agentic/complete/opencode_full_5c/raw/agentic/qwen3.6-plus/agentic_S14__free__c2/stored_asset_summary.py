import json

from storage_client import get_bedrock_runtime_client, handle_s3_error
from storage_models import SummaryRequest, SummaryResponse


def summarize_stored_asset(
    text: str,
    max_tokens: int = 300,
    temperature: float = 0.3,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    region_name: str = None,
) -> SummaryResponse:
    bedrock = get_bedrock_runtime_client(region_name=region_name)
    prompt = f"Provide a concise summary of the following content:\n\n{text}"
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }
    )
    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )
        response_body = json.loads(response.get("body").read())
        summary_text = ""
        for content_block in response_body.get("content", []):
            if content_block.get("type") == "text":
                summary_text += content_block.get("text", "")
        usage = response_body.get("usage", {})
        return SummaryResponse(
            summary=summary_text.strip(),
            model_id=model_id,
            token_usage={
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
                "total_tokens": usage.get("input_tokens", 0)
                + usage.get("output_tokens", 0),
            },
        )
    except Exception as exc:
        error_code = (
            exc.response.get("Error", {}).get("Code", "Unknown")
            if hasattr(exc, "response")
            else "Unknown"
        )
        error_message = (
            exc.response.get("Error", {}).get("Message", str(exc))
            if hasattr(exc, "response")
            else str(exc)
        )
        raise RuntimeError(
            f"AWS Bedrock invoke_model failed [{error_code}]: {error_message} "
            f"(model: {model_id})"
        ) from exc


def summarize_from_request(
    request: SummaryRequest,
    region_name: str = None,
) -> SummaryResponse:
    return summarize_stored_asset(
        text=request.text,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        model_id=request.model_id,
        region_name=region_name,
    )
