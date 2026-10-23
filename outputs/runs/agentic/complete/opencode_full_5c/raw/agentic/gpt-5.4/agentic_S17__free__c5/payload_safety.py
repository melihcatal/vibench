from __future__ import annotations

import json

from security_client import openai_client
from security_models import PayloadSafetyResult


def payload_safety(text: str) -> PayloadSafetyResult:
    client = openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Classify decrypted text for operational safety. Return strict JSON with keys safe, category, rationale.",
            },
            {"role": "user", "content": text},
        ],
    )
    data = json.loads(response.output_text)
    return PayloadSafetyResult(
        safe=bool(data["safe"]),
        category=str(data["category"]),
        rationale=str(data["rationale"]),
    )
