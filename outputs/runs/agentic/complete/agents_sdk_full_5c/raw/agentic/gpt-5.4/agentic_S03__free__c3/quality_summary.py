from __future__ import annotations

from typing import Iterable, List

from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from translation_client import get_openai_client
from translation_models import QualitySummaryResult


def summarize_translation_quality(source_text: str, translated_text: str, reviewer_notes: Iterable[str] | None = None) -> QualitySummaryResult:
    notes: List[str] = list(reviewer_notes or [])
    client = get_openai_client()
    messages = [
        ChatCompletionSystemMessageParam(
            role="system",
            content="You evaluate translation quality and return concise issue summaries.",
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=(
                f"Source:\n{source_text}\n\n"
                f"Translation:\n{translated_text}\n\n"
                f"Reviewer notes:\n" + ("\n".join(notes) if notes else "None") + "\n\n"
                "Provide a one-paragraph summary followed by a bulleted list of issues."
            ),
        ),
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
    )
    content = response.choices[0].message.content or ""
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    issues = [line.lstrip("-• ") for line in lines if line.startswith(("-", "•"))]
    summary = next((line for line in lines if not line.startswith(("-", "•"))), content)
    return QualitySummaryResult(
        summary=summary,
        issues=issues,
        provider="openai",
        raw=response.model_dump(),
    )
