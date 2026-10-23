from __future__ import annotations

import re

from openai import OpenAI

from security_models import SafetyReport

MODEL_ID = "gpt-4o-mini"
UNSAFE_PATTERN = re.compile(r"(password|token|secret|drop\s+table|rm\s+-rf)", re.IGNORECASE)


def check_label_safety(label: str, note: str) -> SafetyReport:
    client = OpenAI()
    moderation_prompt = f"Evaluate whether this secret label and note are safe for operational use: label={label!r}, note={note!r}."
    llm_result = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Return only a brief safety assessment."},
            {"role": "user", "content": moderation_prompt},
        ],
    )
    reasons = []
    text = f"{label} {note}"
    if UNSAFE_PATTERN.search(text):
        reasons.append("contains sensitive or dangerous wording")
    content = llm_result.choices[0].message.content or ""
    is_safe = not reasons and ("unsafe" not in content.lower())
    return SafetyReport(label=label, note=note, is_safe=is_safe, reasons=reasons)
