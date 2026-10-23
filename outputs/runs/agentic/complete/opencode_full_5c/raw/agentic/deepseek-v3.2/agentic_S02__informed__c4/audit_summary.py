import os
from anthropic import Anthropic
from typing import List, Dict, Any
from datetime import datetime


def summarize_login_audit_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    events_text = "\n".join(
        [
            f"Event {i + 1}: User={e.get('user_id', 'unknown')}, "
            f"Provider={e.get('provider', 'unknown')}, "
            f"Time={e.get('timestamp', 'unknown')}, "
            f"Status={e.get('status', 'unknown')}, "
            f"IP={e.get('ip_address', 'unknown')}"
            for i, e in enumerate(events)
        ]
    )

    prompt = f"""You are analyzing federated login audit events. Here are the recent login events:

{events_text}

Please provide a concise summary that includes:
1. Total number of login attempts
2. Breakdown by identity provider (Auth0, Cognito, Azure, etc.)
3. Success vs failure rates
4. Any suspicious patterns (multiple failures from same IP, unusual times, etc.)
5. Recommendations for security improvements

Format the response as a JSON object with these keys: total_attempts, provider_breakdown, success_rate, failure_rate, suspicious_patterns, recommendations."""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        import json

        try:
            summary_json = json.loads(summary_text)
        except json.JSONDecodeError:
            summary_json = {
                "total_attempts": len(events),
                "provider_breakdown": {},
                "success_rate": 0,
                "failure_rate": 0,
                "suspicious_patterns": ["Unable to parse AI response"],
                "recommendations": ["Check audit logs manually"],
                "raw_summary": summary_text,
            }

        success_count = sum(1 for e in events if e.get("status") == "success")
        failure_count = sum(1 for e in events if e.get("status") == "failure")

        provider_counts = {}
        for e in events:
            provider = e.get("provider", "unknown")
            provider_counts[provider] = provider_counts.get(provider, 0) + 1

        summary_json.update(
            {
                "total_attempts": len(events),
                "success_count": success_count,
                "failure_count": failure_count,
                "success_rate": (success_count / len(events) * 100) if events else 0,
                "failure_rate": (failure_count / len(events) * 100) if events else 0,
                "provider_counts": provider_counts,
                "analyzed_at": datetime.now().isoformat(),
                "model_used": "claude-3-5-sonnet-20241022",
            }
        )

        return summary_json

    except Exception as e:
        raise Exception(f"Failed to generate audit summary with Anthropic: {str(e)}")


if __name__ == "__main__":
    sample_events = [
        {
            "user_id": "user123",
            "provider": "auth0",
            "timestamp": "2024-01-15T10:30:00Z",
            "status": "success",
            "ip_address": "192.168.1.100",
        },
        {
            "user_id": "user456",
            "provider": "cognito",
            "timestamp": "2024-01-15T11:15:00Z",
            "status": "failure",
            "ip_address": "192.168.1.101",
        },
        {
            "user_id": "user789",
            "provider": "auth0",
            "timestamp": "2024-01-15T12:00:00Z",
            "status": "success",
            "ip_address": "192.168.1.100",
        },
    ]

    summary = summarize_login_audit_events(sample_events)
    print(f"Audit Summary:")
    print(f"Total attempts: {summary['total_attempts']}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    print(f"Provider breakdown: {summary['provider_counts']}")
