from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from database_models import success_response, error_response

OPENAI_MODEL = "gpt-4o-mini"


async def record_translate(request: Dict[str, Any]) -> Dict[str, Any]:
    text = request.get("text", "")
    target_language = request.get("target_language", "en")
    if not isinstance(text, str):
        return error_response("text must be a string")
    client = OpenAI()
    prompt = f"Translate the following user-facing document text into {target_language}:\n{text}"
    try:
        completion = client.responses.create(model=OPENAI_MODEL, input=prompt)
        return success_response({"translation": completion.output_text, "target_language": target_language})
    except Exception as exc:
        return error_response(str(exc), code="provider_error")
