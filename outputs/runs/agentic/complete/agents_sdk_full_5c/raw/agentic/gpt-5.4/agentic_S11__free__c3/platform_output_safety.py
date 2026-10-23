from __future__ import annotations

import json

from model_client import get_azure_openai_client
from model_models import SafetyAssessment
from select_platform_resource import select_platform_resource


SAFETY_SYSTEM_PROMPT = (
    "You are an Azure OpenAI safety reviewer. "
    "Classify whether the assistant output is unsafe. "
    "Return strict JSON with keys flagged and categories."
)


def check_platform_output_safety(text: str) -> SafetyAssessment:
    client = get_azure_openai_client()
    resource = select_platform_resource(task="safety")
    response = client.chat.completions.create(
        model=resource.deployment_name or resource.model_id,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SAFETY_SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0,
        max_tokens=120,
    )
    payload = json.loads(response.choices[0].message.content or "{}")
    return SafetyAssessment(
        flagged=bool(payload.get("flagged", False)),
        categories=list(payload.get("categories", [])),
        raw=response,
    )
