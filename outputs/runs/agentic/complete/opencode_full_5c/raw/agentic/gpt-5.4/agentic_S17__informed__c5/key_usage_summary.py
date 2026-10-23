from __future__ import annotations

import json

from security_client import OPENAI_PROVIDER, OPENAI_SUMMARY_MODEL, get_openai_client
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse


def key_usage_summary(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_SUMMARY_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize key usage and cryptographic events with notable anomalies, volume, and compliance-relevant observations.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(request.events, ensure_ascii=False),
                    }
                ],
            },
        ],
    )
    return KeyUsageSummaryResponse(
        provider=OPENAI_PROVIDER,
        model=OPENAI_SUMMARY_MODEL,
        summary=response.output_text,
    )
