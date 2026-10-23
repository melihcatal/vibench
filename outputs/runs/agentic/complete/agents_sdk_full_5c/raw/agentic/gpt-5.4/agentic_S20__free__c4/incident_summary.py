from __future__ import annotations

from typing import Dict, List

from openai import OpenAI

from observability_models import NormalizedLogRecord, summarize_records


OPENAI_MODEL = "gpt-4o-mini"


def incident_summary(records: List[NormalizedLogRecord]) -> str:
    client = OpenAI()
    stats: Dict[str, object] = summarize_records(records)
    lines = [f"{record.timestamp} | {record.severity} | {record.service} | {record.message}" for record in records[:20]]
    prompt = (
        "Summarize these Datadog error logs for incident review. Include impact, likely pattern, and next steps.\n"
        f"Aggregate stats: {stats}\n"
        "Logs:\n" + "\n".join(lines)
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text
