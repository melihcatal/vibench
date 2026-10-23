import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-5.4-mini")


@dataclass
class MessageSummaryRequest:
    messages: List[Dict[str, Any]]
    tone: str = "concise"


@dataclass
class MessageSummaryResult:
    summary: str
    message_count: int
    successful_count: int
    failed_count: int
    provider: str = "openai"
    model: str = OPENAI_MODEL


def _normalize_messages(messages: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for message in messages:
        if not isinstance(message, dict):
            continue
        normalized.append(
            {
                "id": message.get("id") or message.get("message_id") or message.get("event_id"),
                "status": message.get("status") or message.get("result") or "unknown",
                "detail": message.get("detail") or message.get("error") or message.get("summary") or "",
            }
        )
    return normalized


def summarize_message_processing_results(messages: Iterable[Dict[str, Any]], tone: str = "concise") -> MessageSummaryResult:
    client = OpenAI()
    normalized = _normalize_messages(messages)
    successful_count = sum(1 for item in normalized if str(item["status"]).lower() in {"ok", "success", "succeeded", "processed", "done"})
    failed_count = sum(1 for item in normalized if str(item["status"]).lower() in {"failed", "error", "rejected", "dead_lettered"})
    prompt = {
        "tone": tone,
        "messages": normalized,
        "instructions": "Summarize the processing results in one short paragraph. Mention overall outcomes, notable failures, and any repeated patterns.",
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You summarize message processing results for operational reporting.",
            },
            {
                "role": "user",
                "content": json.dumps(prompt, ensure_ascii=False),
            },
        ],
    )
    summary_text = getattr(response, "output_text", None) or ""
    if not summary_text and getattr(response, "output", None):
        parts: List[str] = []
        for item in response.output:
            for content in getattr(item, "content", []) or []:
                text = getattr(content, "text", None)
                if text:
                    parts.append(text)
        summary_text = "".join(parts)
    return MessageSummaryResult(
        summary=summary_text.strip(),
        message_count=len(normalized),
        successful_count=successful_count,
        failed_count=failed_count,
    )


def summarize_from_json(payload: str) -> MessageSummaryResult:
    data = json.loads(payload)
    messages = data.get("messages", [])
    tone = data.get("tone", "concise")
    return summarize_message_processing_results(messages=messages, tone=tone)
