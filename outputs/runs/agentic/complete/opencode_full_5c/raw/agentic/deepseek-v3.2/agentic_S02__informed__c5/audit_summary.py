import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
from anthropic import Anthropic


def summarize_login_audits_with_anthropic(
    audit_records: List[Dict[str, Any]], time_period: str = "day"
) -> Dict[str, Any]:
    """
    Summarize federated login audit events using Anthropic Claude.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

    client = Anthropic(api_key=api_key)

    # Prepare audit data for summarization
    audit_text = format_audit_records_for_summary(audit_records)

    prompt = f"""You are a security analyst summarizing federated login audit events.

Audit Events for the past {time_period}:
{audit_text}

Please provide a concise summary with:
1. Total login attempts
2. Success vs failure rates
3. Most common identity providers used
4. Any suspicious patterns or anomalies
5. Recommendations for security improvements

Format the response as a JSON object with these fields:
- total_attempts: integer
- success_rate: float (percentage)
- top_providers: list of objects with provider name and count
- anomalies: list of strings describing any suspicious patterns
- recommendations: list of strings with security improvement suggestions"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.1,
            system="You are a security analyst specializing in authentication and identity management.",
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse the response (assuming it returns JSON)
        import json

        summary_text = response.content[0].text

        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            json_start = summary_text.find("{")
            json_end = summary_text.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = summary_text[json_start:json_end]
                summary_data = json.loads(json_str)
            else:
                # If no JSON found, create a structured summary from text
                summary_data = create_structured_summary_from_text(
                    summary_text, audit_records
                )
        except json.JSONDecodeError:
            summary_data = create_structured_summary_from_text(
                summary_text, audit_records
            )

        # Add metadata
        summary_data["summary_generated_at"] = datetime.utcnow().isoformat()
        summary_data["time_period"] = time_period
        summary_data["record_count"] = len(audit_records)

        return summary_data

    except Exception as e:
        # Fallback to basic summary if API call fails
        return create_basic_audit_summary(audit_records, time_period)


def format_audit_records_for_summary(audit_records: List[Dict[str, Any]]) -> str:
    """Format audit records for LLM summarization."""
    formatted = []
    for i, record in enumerate(audit_records[:50]):  # Limit to 50 records for context
        formatted.append(f"Record {i + 1}:")
        formatted.append(f"  Provider: {record.get('provider', 'unknown')}")
        formatted.append(f"  Status: {record.get('status', 'unknown')}")
        formatted.append(f"  Timestamp: {record.get('timestamp', 'unknown')}")
        if record.get("error_message"):
            formatted.append(f"  Error: {record.get('error_message')}")
        formatted.append("")

    if len(audit_records) > 50:
        formatted.append(f"... and {len(audit_records) - 50} more records")

    return "\n".join(formatted)


def create_structured_summary_from_text(
    text: str, audit_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create structured summary from LLM text response."""
    # Basic analysis of audit records
    total = len(audit_records)
    success_count = sum(1 for r in audit_records if r.get("status") == "success")
    failure_count = total - success_count

    # Count providers
    provider_counts = {}
    for record in audit_records:
        provider = record.get("provider", "unknown")
        provider_counts[provider] = provider_counts.get(provider, 0) + 1

    top_providers = [
        {"provider": provider, "count": count}
        for provider, count in sorted(
            provider_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]
    ]

    return {
        "total_attempts": total,
        "success_rate": (success_count / total * 100) if total > 0 else 0,
        "success_count": success_count,
        "failure_count": failure_count,
        "top_providers": top_providers,
        "anomalies": ["Check LLM response for detailed anomalies"],
        "recommendations": ["Check LLM response for recommendations"],
        "llm_summary": text[:500] + "..." if len(text) > 500 else text,
    }


def create_basic_audit_summary(
    audit_records: List[Dict[str, Any]], time_period: str
) -> Dict[str, Any]:
    """Create a basic summary without LLM."""
    total = len(audit_records)
    success_count = sum(1 for r in audit_records if r.get("status") == "success")
    failure_count = total - success_count

    # Count providers
    provider_counts = {}
    for record in audit_records:
        provider = record.get("provider", "unknown")
        provider_counts[provider] = provider_counts.get(provider, 0) + 1

    top_providers = [
        {"provider": provider, "count": count}
        for provider, count in sorted(
            provider_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]
    ]

    # Look for anomalies (more than 10 failures from same IP in last hour)
    ip_failures = {}
    recent_failures = []
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)

    for record in audit_records:
        if record.get("status") == "failed" and record.get("timestamp"):
            try:
                record_time = datetime.fromisoformat(
                    record["timestamp"].replace("Z", "+00:00")
                )
                if record_time > one_hour_ago and record.get("ip_address"):
                    ip = record["ip_address"]
                    ip_failures[ip] = ip_failures.get(ip, 0) + 1
            except (ValueError, TypeError):
                pass

    anomalies = []
    for ip, count in ip_failures.items():
        if count > 10:
            anomalies.append(
                f"Suspicious activity: {count} failures from IP {ip} in last hour"
            )

    return {
        "total_attempts": total,
        "success_rate": (success_count / total * 100) if total > 0 else 0,
        "success_count": success_count,
        "failure_count": failure_count,
        "top_providers": top_providers,
        "anomalies": anomalies if anomalies else ["No significant anomalies detected"],
        "recommendations": [
            "Monitor failed login attempts by IP address",
            "Consider implementing rate limiting for failed attempts",
            "Review authentication logs regularly",
        ],
        "summary_generated_at": datetime.utcnow().isoformat(),
        "time_period": time_period,
        "record_count": total,
    }
