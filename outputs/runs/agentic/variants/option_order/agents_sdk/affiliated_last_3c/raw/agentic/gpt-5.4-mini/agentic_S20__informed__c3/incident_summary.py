from __future__ import annotations

from anthropic import Anthropic

from observability_models import IncidentSummary


client = Anthropic()


def incident_summary(log_findings: list[str], severity: str = "high") -> IncidentSummary:
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[
            {"role": "user", "content": "Summarize these error-log findings for incident review:\n" + "\n".join(log_findings)}
        ],
    )
    text = response.content[0].text if response.content else ""
    affected_services = ["observability"]
    return IncidentSummary(title="Incident review summary", severity=severity, affected_services=affected_services, key_findings=[text], raw=response)
