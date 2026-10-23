"""
Summarize federated-login audit events using OpenAI.

Provider: OpenAI Chat Completions API
Model: gpt-4o
Environment variable: OPENAI_API_KEY

Takes a list of federated-login audit events and generates
a human-readable summary with patterns, anomalies, and key metrics.
"""

from __future__ import annotations

import json
from typing import Optional

from openai import OpenAI


class AuditEventSummarizer:
    """Summarizes federated-login audit events using OpenAI GPT-4o."""

    SYSTEM_PROMPT = """You are a security analyst specializing in federated identity and authentication.
Analyze the provided federated-login audit events and produce a concise summary that includes:

1. Key metrics: total logins, success rate, unique users, providers used
2. Anomalies or suspicious patterns: failed login spikes, unusual geolocations, new providers
3. Provider distribution: breakdown of which identity providers were used
4. Recommendations: any security concerns or suggested actions

Keep the summary professional, actionable, and under 400 words.
Use bullet points for readability.
"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
    ):
        self.model = model
        self.client = OpenAI(
            api_key=api_key,
        )

    def summarize(
        self,
        audit_events: list[dict],
        time_range: Optional[str] = None,
        max_events: int = 100,
    ) -> str:
        """
        Summarize federated-login audit events using OpenAI GPT-4o.

        Args:
            audit_events: List of audit event dicts with fields like
                event_type, timestamp, user_id, provider, status, ip, etc.
            time_range: Optional description of the time window
            max_events: Maximum number of events to include

        Returns:
            A human-readable summary string.
        """
        events = audit_events[:max_events]
        events_json = json.dumps(events, indent=2, default=str)

        time_context = f"Time range: {time_range}" if time_range else ""

        user_message = f"""{time_context}

Here are {len(events)} federated-login audit events to analyze:

{events_json}

Please provide a security-focused summary of these events.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        summary = response.choices[0].message.content
        return summary or "No summary generated."

    def summarize_with_insights(
        self,
        audit_events: list[dict],
        include_recommendations: bool = True,
    ) -> dict:
        """
        Summarize events and return structured output with key insights.

        Returns a dict with 'summary', 'key_metrics', and 'recommendations'.
        """
        events_json = json.dumps(audit_events[:100], indent=2, default=str)

        prompt = f"""Analyze these federated-login audit events from Auth0 and return a JSON object with:
- "summary": a brief text summary
- "key_metrics": object with total_logins, success_count, failure_count, unique_users, providers_used
- "recommendations": list of security recommendations

Events:
{events_json}

Return valid JSON only.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a security analyst. Return valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=1000,
            response_format={"type": "json_object"},
        )

        result_text = response.choices[0].message.content
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            return {
                "summary": result_text,
                "key_metrics": {},
                "recommendations": [],
            }


def summarize_audit_events(
    audit_events: list[dict],
    time_range: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Convenience function to summarize federated-login audit events using OpenAI.

    Returns a human-readable summary string.
    """
    summarizer = AuditEventSummarizer(api_key=api_key)
    return summarizer.summarize(audit_events, time_range=time_range)


if __name__ == "__main__":
    sample_events = [
        {
            "event_type": "login_success",
            "timestamp": "2024-01-15T10:30:00Z",
            "user_id": "auth0|user123",
            "provider": "google-oauth2",
            "ip": "192.168.1.1",
        },
        {
            "event_type": "login_failure",
            "timestamp": "2024-01-15T10:31:00Z",
            "user_id": "auth0|user456",
            "provider": "auth0",
            "ip": "10.0.0.1",
            "reason": "invalid_credentials",
        },
    ]
    summary = summarize_audit_events(sample_events)
    print(summary)
