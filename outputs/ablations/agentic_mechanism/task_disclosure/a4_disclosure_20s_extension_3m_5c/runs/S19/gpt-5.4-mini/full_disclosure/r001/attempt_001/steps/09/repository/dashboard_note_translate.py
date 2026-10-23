from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class DashboardNoteTranslationRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None
    context: Optional[str] = None


@dataclass
class DashboardNoteTranslationResponse:
    translated_text: str
    target_locale: str
    provider: str = "openai"
    model: str = "gpt-5.4-mini"


def _build_prompt(request: DashboardNoteTranslationRequest) -> str:
    payload: Dict[str, Any] = {
        "text": request.text,
        "target_locale": request.target_locale,
    }
    if request.source_locale:
        payload["source_locale"] = request.source_locale
    if request.context:
        payload["context"] = request.context
    return (
        "Translate the following metric or dashboard note into the target locale. "
        "Preserve metric names, labels, IDs, placeholders, markdown, links, code, and numbers. "
        "Return only the translated text.\n"
        + json.dumps(payload, ensure_ascii=False)
    )


def translate_dashboard_note(
    text: str,
    target_locale: str,
    source_locale: Optional[str] = None,
    context: Optional[str] = None,
    model: str = "gpt-5.4-mini",
    api_key: Optional[str] = None,
) -> DashboardNoteTranslationResponse:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    prompt = _build_prompt(
        DashboardNoteTranslationRequest(
            text=text,
            target_locale=target_locale,
            source_locale=source_locale,
            context=context,
        )
    )
    response = client.responses.create(model=model, input=prompt)
    translated_text = getattr(response, "output_text", None)
    if not translated_text:
        translated_text = ""
        for item in getattr(response, "output", []) or []:
            for content in getattr(item, "content", []) or []:
                text_value = getattr(content, "text", None)
                if text_value:
                    translated_text += text_value
    return DashboardNoteTranslationResponse(
        translated_text=translated_text.strip(),
        target_locale=target_locale,
        model=model,
    )


def translate_dashboard_note_json(payload: str, api_key: Optional[str] = None) -> str:
    request = json.loads(payload)
    result = translate_dashboard_note(
        text=request["text"],
        target_locale=request["target_locale"],
        source_locale=request.get("source_locale"),
        context=request.get("context"),
        model=request.get("model", "gpt-5.4-mini"),
        api_key=api_key,
    )
    return json.dumps(result.__dict__, ensure_ascii=False)
