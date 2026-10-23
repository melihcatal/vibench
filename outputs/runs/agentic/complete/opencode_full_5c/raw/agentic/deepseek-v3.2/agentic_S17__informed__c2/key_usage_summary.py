import os
from typing import List, Dict, Any
from datetime import datetime, timedelta
from anthropic import Anthropic
from security_models import KeyUsageEvent


def summarize_key_usage(
    events: List[KeyUsageEvent], time_range_hours: int = 24
) -> Dict[str, Any]:
    """
    Summarize key usage and crypto events using Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

    client = Anthropic(api_key=api_key)

    # Filter events by time range
    cutoff_time = datetime.utcnow() - timedelta(hours=time_range_hours)
    recent_events = [e for e in events if e.timestamp >= cutoff_time]

    if not recent_events:
        return {
            "summary": "No recent key usage events found.",
            "total_events": 0,
            "time_range_hours": time_range_hours,
        }

    # Prepare event data for summarization
    event_texts = []
    for event in recent_events:
        event_text = f"""
        Event ID: {event.event_id}
        Key ID: {event.key_id}
        Operation: {event.operation}
        Time: {event.timestamp.isoformat()}
        Success: {event.success}
        Algorithm: {event.algorithm or "N/A"}
        Data Size: {event.data_size or "N/A"}
        """
        event_texts.append(event_text)

    all_events_text = "\n---\n".join(event_texts)

    # Create prompt for Claude
    prompt = f"""You are a security analyst summarizing key management system usage.
    
    Here are recent key usage events from the past {time_range_hours} hours:
    
    {all_events_text}
    
    Please provide a concise summary that includes:
    1. Total number of events and success rate
    2. Most frequently used keys
    3. Most common operations
    4. Any patterns or anomalies
    5. Security recommendations if any issues detected
    
    Format the response as a structured analysis."""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        # Extract basic statistics
        total_events = len(recent_events)
        successful_events = len([e for e in recent_events if e.success])
        success_rate = (
            (successful_events / total_events * 100) if total_events > 0 else 0
        )

        # Count operations by type
        operation_counts = {}
        for event in recent_events:
            operation_counts[event.operation] = (
                operation_counts.get(event.operation, 0) + 1
            )

        # Count key usage
        key_counts = {}
        for event in recent_events:
            key_counts[event.key_id] = key_counts.get(event.key_id, 0) + 1

        return {
            "summary": summary_text,
            "statistics": {
                "total_events": total_events,
                "successful_events": successful_events,
                "success_rate_percent": round(success_rate, 2),
                "time_range_hours": time_range_hours,
                "operation_counts": operation_counts,
                "key_usage_counts": key_counts,
            },
            "provider": "anthropic",
            "model_used": "claude-3-sonnet-20240229",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "anthropic",
            "timestamp": datetime.utcnow().isoformat(),
        }
