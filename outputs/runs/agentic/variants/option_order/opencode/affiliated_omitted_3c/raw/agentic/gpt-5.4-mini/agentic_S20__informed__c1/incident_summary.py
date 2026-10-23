from dataclasses import dataclass
from typing import Any, Dict, List

import anthropic


@dataclass
class IncidentSummary:
    summary: str
    findings: List[Dict[str, Any]]


def build_summary(findings: List[Dict[str, Any]]) -> IncidentSummary:
    client = anthropic.Anthropic(api_key=None)
    prompt = f"Summarize these error log findings for incident review: {findings}"
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text = message.content[0].text if message.content else ""
    return IncidentSummary(summary=text, findings=findings)
