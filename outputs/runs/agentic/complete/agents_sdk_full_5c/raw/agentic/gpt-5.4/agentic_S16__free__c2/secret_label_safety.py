from __future__ import annotations

from typing import Iterable

import openai

from security_models import SafetyCheckResult


OPENAI_MODEL = "gpt-4o-mini"
UNSAFE_TERMS = ("password", "secret", "private key", "token", "credential")


def check_label_safety(labels: Iterable[str], notes: str) -> SafetyCheckResult:
    text = "\n".join(list(labels) + [notes])
    client = openai.OpenAI()
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    findings: list[str] = []
    for term in UNSAFE_TERMS:
        if term in text.lower():
            findings.append(f"contains sensitive term: {term}")

    moderation = response.results[0]
    if moderation.flagged:
        findings.append("OpenAI moderation flagged the content")

    return SafetyCheckResult(safe=not findings, findings=findings)
