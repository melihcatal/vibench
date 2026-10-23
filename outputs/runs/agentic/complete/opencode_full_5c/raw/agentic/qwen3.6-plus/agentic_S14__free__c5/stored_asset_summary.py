import json
from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_bedrock_runtime_client, handle_aws_error
from storage_models import StorageConfig, SummaryRequest, SummaryResponse


def summarize_stored_asset(
    text: str,
    max_length: int = 300,
    min_length: int = 50,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    config: Optional[StorageConfig] = None,
) -> SummaryResponse:
    bedrock_client = get_bedrock_runtime_client(config)

    prompt = (
        f"Summarize the following content in {min_length} to {max_length} words. "
        f"Focus on the key points and main ideas.\n\n"
        f"Content:\n{text}\n\n"
        f"Summary:"
    )

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.3,
        }
    )

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        response_body = json.loads(response.get("body").read())

        summary_text = ""
        token_count = 0

        if "content" in response_body:
            for content_block in response_body["content"]:
                if content_block.get("type") == "text":
                    summary_text += content_block.get("text", "")

        if "usage" in response_body:
            token_count = response_body["usage"].get("output_tokens", 0)

        return SummaryResponse(
            success=True,
            summary=summary_text.strip(),
            model_id=model_id,
            token_count=token_count,
        )

    except ClientError as e:
        return SummaryResponse(
            success=False,
            model_id=model_id,
            error=handle_aws_error(e, "summarize_stored_asset"),
        )
    except Exception as e:
        return SummaryResponse(
            success=False,
            model_id=model_id,
            error=f"summarize_stored_asset error: {str(e)}",
        )


def summarize_from_request(
    request: SummaryRequest,
    config: Optional[StorageConfig] = None,
) -> SummaryResponse:
    return summarize_stored_asset(
        text=request.text,
        max_length=request.max_length,
        min_length=request.min_length,
        model_id=request.model_id,
        config=config,
    )


def summarize_ocr_result(
    ocr_text: str,
    max_length: int = 300,
    min_length: int = 50,
    config: Optional[StorageConfig] = None,
) -> SummaryResponse:
    return summarize_stored_asset(
        text=ocr_text,
        max_length=max_length,
        min_length=min_length,
        config=config,
    )
