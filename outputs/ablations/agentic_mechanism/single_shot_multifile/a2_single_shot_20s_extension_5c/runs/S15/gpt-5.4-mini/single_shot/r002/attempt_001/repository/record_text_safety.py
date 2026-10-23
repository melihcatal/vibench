from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from database_models import success_response, error_response

OPENAI_MODEL = "gpt-4o-mini"


async def record_text_safety(request: Dict[str, Any]) -> Dict[str, Any]:
    text = request.get("text", "")
    if not isinstance(text, str):
        return error_response("text must be a string")
    client = OpenAI()
    prompt = "Assess whether the following user-generated document text is unsafe, and return a short verdict with reasons. Text:\n" + text
    try:
        completion = client.responses.create(model=OPENAI_MODEL, input=prompt)
        return success_response({"analysis": completion.output_text})
    except Exception as exc:
        return error_response(str(exc), code="provider_error")
