from __future__ import annotations

import json
import os
from typing import Iterable

from openai import OpenAI

from identity_models import AuditRecord, AuditSummary, model_dump


OPENAI_MODEL = "gpt-4o-mini"


def summarize_audit_events(events: Iterable[AuditRecord]) -> AuditSummary:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    serialized = [model_dump(event) for event in events]
    prompt = (
        "Summarize these federated login audit events for a security analyst. "
        "Include suspicious patterns, login success/failure trends, and notable identities.\n\n"
        f"Events:\n{json.dumps(serialized, ensure_ascii=False)}"
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        max_output_tokens=220,
    )
    summary_text = response.output_text
    return AuditSummary(summary_text=summary_text, provider=f"openai:{OPENAI_MODEL}", raw=response.model_dump())
