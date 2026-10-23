"""
Summarizes error-log findings for incident review.

Uses the Anthropic Messages API (api.anthropic.com) to generate
a structured incident summary from error log entries.
Auth: ANTHROPIC_API_KEY environment variable.
"""

import json
import os
from typing import Optional

from anthropic import Anthropic

ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def build_incident_prompt(error_logs: list[dict], context: Optional[str] = None) -> str:
    """Build a prompt for the Anthropic Claude model to generate an incident summary."""
    log_entries_text = ""
    for i, entry in enumerate(error_logs, 1):
        log_entries_text += (
            f"{i}. [{entry.get('status', 'unknown')}] "
            f"{entry.get('timestamp', 'unknown')} | "
            f"Service: {entry.get('service', 'unknown')} | "
            f"Host: {entry.get('hostname', 'unknown')}\n"
            f"   Message: {entry.get('message', '')}\n"
        )

    context_block = ""
    if context:
        context_block = f"\nAdditional context:\n{context}\n"

    prompt = f"""You are an incident response analyst. Review the following error log entries and produce a concise incident summary.

Error Log Entries:
{log_entries_text}
{context_block}

Please provide the incident summary in the following JSON format:
{{
  "incident_title": "Brief descriptive title",
  "severity": "critical|high|medium|low",
  "affected_services": ["service1", "service2"],
  "root_cause_hypothesis": "Analysis of likely root cause",
  "timeline": "Summary of when errors began and their pattern",
  "impact_assessment": "Description of user/system impact",
  "recommended_actions": ["action 1", "action 2", "action 3"],
  "related_correlation_ids": ["id1", "id2"]
}}

Only output valid JSON. Do not include any text before or after the JSON object."""
    return prompt


def summarize_incident(
    error_logs: list[dict],
    context: Optional[str] = None,
    model: str = ANTHROPIC_MODEL,
) -> dict:
    """Summarize error log entries into an incident review using Anthropic Claude.

    Calls the Anthropic Messages API at api.anthropic.com using the
    anthropic SDK with model claude-3-5-sonnet-20241022.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)
    prompt = build_incident_prompt(error_logs, context)

    message = client.messages.create(
        model=model,
        max_tokens=2048,
        system="You are an expert incident response analyst who produces structured incident summaries from raw log data.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    response_text = message.content[0].text.strip()

    # Parse JSON from response
    if response_text.startswith("```json"):
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif response_text.startswith("```"):
        response_text = response_text.split("```")[1].split("```")[0].strip()

    summary = json.loads(response_text)
    return summary


def format_incident_summary(summary: dict) -> str:
    """Format the incident summary for human-readable output."""
    lines = [
        "=" * 60,
        "INCIDENT SUMMARY",
        "=" * 60,
        f"Title: {summary.get('incident_title', 'N/A')}",
        f"Severity: {summary.get('severity', 'N/A').upper()}",
        "",
        "Affected Services:",
    ]
    for svc in summary.get("affected_services", []):
        lines.append(f"  - {svc}")

    lines.extend([
        "",
        "Root Cause Hypothesis:",
        f"  {summary.get('root_cause_hypothesis', 'N/A')}",
        "",
        "Timeline:",
        f"  {summary.get('timeline', 'N/A')}",
        "",
        "Impact Assessment:",
        f"  {summary.get('impact_assessment', 'N/A')}",
        "",
        "Recommended Actions:",
    ])
    for action in summary.get("recommended_actions", []):
        lines.append(f"  - {action}")

    related_ids = summary.get("related_correlation_ids", [])
    if related_ids:
        lines.extend([
            "",
            "Related Correlation IDs:",
        ])
        for cid in related_ids:
            lines.append(f"  - {cid}")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    """Entry point for generating an incident summary from error logs."""
    error_logs = [
        {
            "timestamp": "2025-01-15T10:23:45.123Z",
            "status": "error",
            "service": "api-gateway",
            "hostname": "prod-gw-01",
            "message": "Connection timeout to downstream service after 30s retry exhausted",
        },
        {
            "timestamp": "2025-01-15T10:23:47.456Z",
            "status": "error",
            "service": "payment-service",
            "hostname": "prod-pay-03",
            "message": "Database connection pool exhausted - max connections reached",
        },
        {
            "timestamp": "2025-01-15T10:24:01.789Z",
            "status": "error",
            "service": "api-gateway",
            "hostname": "prod-gw-02",
            "message": "HTTP 502 Bad Gateway returned for /api/v1/checkout endpoint",
        },
        {
            "timestamp": "2025-01-15T10:24:15.012Z",
            "status": "error",
            "service": "payment-service",
            "hostname": "prod-pay-03",
            "message": "Transaction rollback triggered for order batch #4892 due to timeout",
        },
    ]

    context = "The payment processing pipeline has been experiencing intermittent latency spikes since 10:15 UTC. The team has already restarted the payment-service pods but errors persist."

    summary = summarize_incident(error_logs, context)
    print(format_incident_summary(summary))

    print("\n--- Raw JSON ---")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
