import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from identity_models import AuditEvent
import anthropic


def summarize_audit_events(
    events: List[AuditEvent], time_range: str = "day"
) -> Dict[str, Any]:
    """Summarize federated-login audit events using Anthropic Claude."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)

    # Filter events by time range
    now = datetime.now()
    if time_range == "hour":
        cutoff = now - timedelta(hours=1)
    elif time_range == "day":
        cutoff = now - timedelta(days=1)
    elif time_range == "week":
        cutoff = now - timedelta(weeks=1)
    else:
        cutoff = now - timedelta(days=1)

    filtered_events = [e for e in events if e.timestamp >= cutoff]

    if not filtered_events:
        return {
            "summary": "No audit events in the specified time range",
            "total_events": 0,
            "success_rate": 0.0,
            "time_range": time_range,
        }

    # Prepare event data for summarization
    event_texts = []
    for event in filtered_events:
        event_text = f"""
        Event: {event.event_type}
        Time: {event.timestamp.isoformat()}
        User: {event.user_id or "Unknown"}
        Provider: {event.provider}
        Success: {event.success}
        IP: {event.ip_address or "Unknown"}
        """
        if event.details:
            event_text += f"Details: {event.details}"
        event_texts.append(event_text)

    all_events_text = "\n---\n".join(event_texts)

    # Use Anthropic Claude to generate summary
    prompt = f"""You are analyzing login audit events for a federated identity system.
    
Here are the audit events from the last {time_range}:

{all_events_text}

Please provide a concise summary including:
1. Total number of events
2. Success rate (percentage of successful logins)
3. Most common event types
4. Any patterns or anomalies observed
5. Security recommendations if any issues detected

Format your response as a structured JSON with the following fields:
- summary: string (brief overall summary)
- total_events: integer
- successful_logins: integer
- failed_logins: integer
- success_rate: float (percentage)
- top_event_types: list of objects with 'type' and 'count' fields
- patterns: list of strings describing any patterns
- recommendations: list of strings with security recommendations
- time_range: string

Be factual and concise."""

    try:
        # Call Anthropic Claude API
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.1,
            system="You are a security analyst summarizing login audit events.",
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse the response (assuming JSON format)
        import json

        summary_data = json.loads(response.content[0].text)

        # Add basic statistics
        total_events = len(filtered_events)
        successful_logins = sum(
            1 for e in filtered_events if e.success and "login" in e.event_type.lower()
        )
        failed_logins = sum(
            1
            for e in filtered_events
            if not e.success and "login" in e.event_type.lower()
        )

        success_rate = (
            (successful_logins / (successful_logins + failed_logins)) * 100
            if (successful_logins + failed_logins) > 0
            else 0.0
        )

        # Count event types
        from collections import Counter

        event_type_counter = Counter(e.event_type for e in filtered_events)
        top_event_types = [
            {"type": event_type, "count": count}
            for event_type, count in event_type_counter.most_common(5)
        ]

        # Ensure summary data has all required fields
        summary_data.update(
            {
                "total_events": total_events,
                "successful_logins": successful_logins,
                "failed_logins": failed_logins,
                "success_rate": round(success_rate, 2),
                "top_event_types": top_event_types,
                "time_range": time_range,
            }
        )

        return summary_data

    except Exception as e:
        # Fallback to basic summary if API call fails
        total_events = len(filtered_events)
        successful_logins = sum(1 for e in filtered_events if e.success)
        failed_logins = total_events - successful_logins
        success_rate = (
            (successful_logins / total_events) * 100 if total_events > 0 else 0.0
        )

        return {
            "summary": f"Basic audit summary for {time_range}",
            "total_events": total_events,
            "successful_logins": successful_logins,
            "failed_logins": failed_logins,
            "success_rate": round(success_rate, 2),
            "top_event_types": [],
            "patterns": ["Unable to generate detailed patterns due to API error"],
            "recommendations": ["Check API connectivity for advanced analysis"],
            "time_range": time_range,
        }
