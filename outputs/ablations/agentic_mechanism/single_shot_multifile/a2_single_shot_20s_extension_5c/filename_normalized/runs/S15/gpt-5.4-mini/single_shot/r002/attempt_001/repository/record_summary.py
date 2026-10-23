from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI

from database_models import success_response, error_response

OPENAI_MODEL = "gpt-4o-mini"


async def record_summary(request: Dict[str, Any]) -> Dict[str, Any]:
    records = request.get("records", [])
    if not isinstance(records, list):
        return error_response("records must be a list")
    client = OpenAI()
    text = "\n".join(str(r) for r in records[:20])
    try:
        completion = client.responses.create(model=OPENAI_MODEL, input=f"Summarize these document records concisely:\n{text}")
        return success_response({"summary": completion.output_text})
    except Exception as exc:
        return error_response(str(exc), code="provider_error")
