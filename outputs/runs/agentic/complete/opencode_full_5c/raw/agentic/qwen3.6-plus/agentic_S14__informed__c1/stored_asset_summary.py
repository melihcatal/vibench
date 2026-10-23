import json

from storage_client import get_bedrock_runtime_client
from storage_models import SummaryRequest, SummaryResponse


def summarize_stored_asset(
    text: str,
    max_tokens: int = 500,
    temperature: float = 0.3,
    summary_type: str = "concise",
) -> SummaryResponse:
    bedrock_client = get_bedrock_runtime_client()

    if not text or not text.strip():
        return SummaryResponse(
            success=False,
            error="Input text is empty",
        )

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    if summary_type == "concise":
        system_prompt = "You are a summarization assistant. Provide a concise summary of the provided content, capturing the key points in a brief format."
    elif summary_type == "detailed":
        system_prompt = "You are a summarization assistant. Provide a detailed summary of the provided content, capturing all important information, context, and nuances."
    elif summary_type == "bullet":
        system_prompt = "You are a summarization assistant. Provide a summary of the provided content as a bulleted list of key points."
    else:
        system_prompt = "You are a summarization assistant. Provide a clear summary of the provided content."

    user_prompt = f"Please summarize the following content:\n\n{text}"

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    }
                ],
            }
        ],
    }

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
        )

        response_body = json.loads(response.get("body").read())

        summary_text = ""
        input_tokens = 0
        output_tokens = 0

        for content_block in response_body.get("content", []):
            if content_block.get("type") == "text":
                summary_text += content_block.get("text", "")

        usage = response_body.get("usage", {})
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        return SummaryResponse(
            success=True,
            summary=summary_text.strip(),
            model_id=model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    except Exception as exc:
        return SummaryResponse(
            success=False,
            error=str(exc),
        )


def summarize_from_request(request: SummaryRequest) -> SummaryResponse:
    return summarize_stored_asset(
        text=request.text,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        summary_type=request.summary_type,
    )
