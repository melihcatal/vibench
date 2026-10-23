from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI

from safety_models import ModerationSummary

OPENAI_MODEL = "gpt-4o-mini"


def summarize_moderation(decisions: List[Dict[str, Any]]) -> ModerationSummary:
    client = OpenAI()
    prompt = f"Summarize these moderation decisions for an operations reviewer: {decisions}"
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    text = response.choices[0].message.content or ""
    unsafe = sum(1 for d in decisions if str(d.get("label", "")).lower() not in {"allow", "safe"})
    return ModerationSummary(total=len(decisions), unsafe=unsafe, details=[{"summary": text}])
