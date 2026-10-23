from __future__ import annotations

from openai import OpenAI

from storage_client import get_openai_api_key
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse


def summarize_stored_asset(
    request: StoredAssetSummaryRequest,
) -> StoredAssetSummaryResponse:
    model = "gpt-4.1-mini"
    client = OpenAI(api_key=get_openai_api_key())
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize extracted storage asset content concisely.",
                    }
                ],
            },
            {"role": "user", "content": [{"type": "input_text", "text": request.text}]},
        ],
        max_output_tokens=request.max_output_tokens,
    )
    return StoredAssetSummaryResponse(
        provider="openai",
        model=model,
        summary=response.output_text,
    )
