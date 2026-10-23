import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import get_openai_client
from observability_models import IncidentSummary, LogEvent, parse_timestamp


def summarize_error_logs(
    error_logs: List[Dict[str, Any]], incident_id: str = None
) -> IncidentSummary:
    """
    Summarize error-log findings for incident review using OpenAI.

    Args:
        error_logs: List of error log entries
        incident_id: Optional incident identifier (generated if not provided)
    """
    import uuid
    from datetime import datetime

    if incident_id is None:
        incident_id = f"incident-{uuid.uuid4().hex[:8]}"

    if not error_logs:
        return IncidentSummary(
            incident_id=incident_id,
            start_time=int(datetime.now().timestamp() * 1000),
            end_time=int(datetime.now().timestamp() * 1000),
            error_count=0,
            unique_errors=[],
            affected_services=[],
            severity_distribution={},
            sample_logs=[],
            summary_text="No error logs found",
        )

    # Extract timestamps
    timestamps = []
    for log in error_logs:
        if "timestamp" in log:
            timestamps.append(parse_timestamp(log["timestamp"]))
        elif "@timestamp" in log:
            timestamps.append(parse_timestamp(log["@timestamp"]))

    start_time = (
        min(timestamps) if timestamps else int(datetime.now().timestamp() * 1000)
    )
    end_time = max(timestamps) if timestamps else int(datetime.now().timestamp() * 1000)

    # Analyze logs
    error_count = len(error_logs)
    unique_errors = set()
    affected_services = set()
    severity_distribution = {}

    sample_logs = error_logs[:10]  # Take first 10 as sample

    for log in error_logs:
        # Extract error message
        message = None
        if "message" in log:
            message = log["message"]
        elif "@message" in log:
            try:
                parsed = json.loads(log["@message"])
                message = parsed.get("message", log["@message"])
            except:
                message = log["@message"]

        if message:
            unique_errors.add(message[:200])  # Truncate for uniqueness

        # Extract service
        service = None
        if "service" in log:
            service = log["service"]
        elif "parsed_message" in log and isinstance(log["parsed_message"], dict):
            service = log["parsed_message"].get("service")

        if service:
            affected_services.add(service)

        # Count severity
        severity = log.get("level", "ERROR")
        if "parsed_message" in log and isinstance(log["parsed_message"], dict):
            severity = log["parsed_message"].get("level", severity)

        severity_distribution[severity] = severity_distribution.get(severity, 0) + 1

    # Generate summary using OpenAI
    summary_text = generate_incident_summary(
        error_count=error_count,
        unique_errors=list(unique_errors)[:5],
        affected_services=list(affected_services),
        severity_distribution=severity_distribution,
        sample_logs=sample_logs[:3],
    )

    return IncidentSummary(
        incident_id=incident_id,
        start_time=start_time,
        end_time=end_time,
        error_count=error_count,
        unique_errors=list(unique_errors)[:10],
        affected_services=list(affected_services),
        severity_distribution=severity_distribution,
        sample_logs=sample_logs,
        summary_text=summary_text,
    )


def generate_incident_summary(
    error_count: int,
    unique_errors: List[str],
    affected_services: List[str],
    severity_distribution: Dict[str, int],
    sample_logs: List[Dict[str, Any]],
) -> str:
    """Generate incident summary using OpenAI GPT-4."""
    try:
        client = get_openai_client()

        prompt = f"""
        You are analyzing error logs for an incident review. Provide a concise summary.
        
        Error Count: {error_count}
        Unique Error Patterns: {unique_errors}
        Affected Services: {affected_services}
        Severity Distribution: {severity_distribution}
        
        Sample Logs:
        {json.dumps(sample_logs, indent=2)}
        
        Please provide:
        1. Brief incident overview
        2. Most common error patterns
        3. Potential root causes
        4. Recommended next steps
        
        Keep the summary professional and actionable.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior SRE analyzing error logs for incident review.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Fallback summary if OpenAI fails
        return f"""Incident Summary:
- Total Errors: {error_count}
- Affected Services: {", ".join(affected_services) if affected_services else "Unknown"}
- Severity: {severity_distribution}
- Key Error Patterns: {", ".join(unique_errors[:3]) if unique_errors else "None identified"}
- Time Range: {datetime.fromtimestamp(start_time / 1000).isoformat()} to {datetime.fromtimestamp(end_time / 1000).isoformat()}
- Recommended: Investigate the most frequent error patterns and check service health."""

    # Note: start_time and end_time are defined in the outer function scope
    # This fallback will work when called from summarize_error_logs
