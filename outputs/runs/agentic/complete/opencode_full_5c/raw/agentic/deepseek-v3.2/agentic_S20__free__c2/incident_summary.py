import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from openai import OpenAI


def incident_summary(
    error_logs: List[Dict[str, Any]],
    hours_back: int = 24,
    service_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Summarize error-log findings for incident review using OpenAI GPT.

    Args:
        error_logs: List of error log entries
        hours_back: Time window for analysis
        service_name: Optional service name for context

    Returns:
        Summary with analysis, patterns, and recommendations
    """
    if not error_logs:
        return {
            "summary": "No error logs found in the specified time window.",
            "error_count": 0,
            "time_window": f"Last {hours_back} hours",
        }

    # Prepare log data for analysis
    log_texts = []
    for log in error_logs[:50]:  # Limit to avoid token limits
        log_text = f"[{log.get('timestamp', '')}] {log.get('severity', '')}: {log.get('message', '')}"
        if "service" in log:
            log_text += f" (Service: {log['service']})"
        if "correlation_id" in log:
            log_text += f" (Correlation: {log['correlation_id']})"
        log_texts.append(log_text)

    logs_for_analysis = "\n".join(log_texts)

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Create prompt for analysis
    prompt = f"""Analyze these error logs from the last {hours_back} hours{f" for service '{service_name}'" if service_name else ""}:

{logs_for_analysis}

Please provide a structured incident summary including:
1. Overall severity assessment (Low/Medium/High/Critical)
2. Top 3-5 most frequent error patterns
3. Timeline of when errors occurred
4. Affected services/components
5. Root cause hypotheses
6. Immediate action recommendations
7. Long-term prevention suggestions

Format the response as a JSON object with these keys:
- "severity_assessment": string
- "error_patterns": list of objects with "pattern", "count", "impact"
- "timeline_analysis": string description
- "affected_services": list
- "root_cause_hypotheses": list of strings
- "immediate_actions": list of strings
- "long_term_recommendations": list of strings
- "summary": brief overall summary string
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced SRE analyzing error logs for incident response.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1500,
        )

        analysis_text = response.choices[0].message.content

        # Try to parse as JSON, fall back to text
        import json

        try:
            analysis = json.loads(analysis_text)
        except json.JSONDecodeError:
            analysis = {"analysis": analysis_text}

        # Add metadata
        result = {
            "summary": analysis.get("summary", "Analysis completed"),
            "error_count": len(error_logs),
            "time_window": f"Last {hours_back} hours",
            "service_filter": service_name,
            "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
            "analysis": analysis,
            "log_sample_count": len(log_texts),
            "total_logs_available": len(error_logs),
        }

        # Add basic statistics
        severity_counts = {}
        service_counts = {}
        for log in error_logs:
            severity = log.get("severity", "UNKNOWN")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            service = log.get("service", "unknown")
            service_counts[service] = service_counts.get(service, 0) + 1

        result["statistics"] = {
            "severity_distribution": severity_counts,
            "service_distribution": service_counts,
            "unique_correlation_ids": len(
                set(
                    log.get("correlation_id")
                    for log in error_logs
                    if log.get("correlation_id")
                )
            ),
        }

        # Add timeline data
        if error_logs:
            timestamps = [
                log.get("timestamp") for log in error_logs if log.get("timestamp")
            ]
            if timestamps:
                try:
                    time_objects = [
                        datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        for ts in timestamps
                    ]
                    result["timeline"] = {
                        "first_error": min(time_objects).isoformat(),
                        "last_error": max(time_objects).isoformat(),
                        "error_rate_per_hour": len(error_logs) / hours_back,
                    }
                except:
                    pass

        return result

    except Exception as e:
        # Fallback to basic analysis if OpenAI fails
        return generate_basic_summary(error_logs, hours_back, service_name)


def generate_basic_summary(
    error_logs: List[Dict[str, Any]],
    hours_back: int,
    service_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate a basic summary when OpenAI is unavailable."""
    severity_counts = {}
    service_counts = {}
    error_messages = {}

    for log in error_logs:
        severity = log.get("severity", "UNKNOWN")
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

        service = log.get("service", "unknown")
        service_counts[service] = service_counts.get(service, 0) + 1

        message = log.get("message", "")
        if message:
            # Simple deduplication by first 50 chars
            key = message[:50]
            error_messages[key] = error_messages.get(
                key, {"message": message, "count": 0, "services": set()}
            )
            error_messages[key]["count"] += 1
            error_messages[key]["services"].add(service)

    # Determine overall severity
    if severity_counts.get("CRITICAL", 0) > 0:
        overall_severity = "CRITICAL"
    elif severity_counts.get("ERROR", 0) > 10:
        overall_severity = "HIGH"
    elif severity_counts.get("ERROR", 0) > 0:
        overall_severity = "MEDIUM"
    else:
        overall_severity = "LOW"

    # Top error patterns
    top_errors = sorted(
        [
            {
                "message": data["message"],
                "count": data["count"],
                "services": list(data["services"]),
            }
            for data in error_messages.values()
        ],
        key=lambda x: x["count"],
        reverse=True,
    )[:5]

    return {
        "summary": f"Found {len(error_logs)} error logs in the last {hours_back} hours",
        "error_count": len(error_logs),
        "time_window": f"Last {hours_back} hours",
        "service_filter": service_name,
        "severity_assessment": overall_severity,
        "statistics": {
            "severity_distribution": severity_counts,
            "service_distribution": service_counts,
            "unique_errors": len(error_messages),
        },
        "top_error_patterns": top_errors,
        "recommendations": [
            "Review the most frequent error patterns above",
            "Check service health metrics for affected services",
            "Consider implementing circuit breakers for frequently failing components",
            "Review recent deployments or configuration changes",
        ],
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    # Example usage with mock data
    mock_logs = [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "severity": "ERROR",
            "message": "Database connection timeout after 30 seconds",
            "service": "user-service",
            "correlation_id": "req-12345",
        },
        {
            "timestamp": "2024-01-15T10:31:00Z",
            "severity": "ERROR",
            "message": "Database connection timeout after 30 seconds",
            "service": "user-service",
            "correlation_id": "req-12346",
        },
        {
            "timestamp": "2024-01-15T10:32:00Z",
            "severity": "CRITICAL",
            "message": "Payment processing failed: insufficient funds",
            "service": "payment-service",
            "correlation_id": "req-12347",
        },
    ]

    summary = incident_summary(mock_logs, hours_back=1, service_name="user-service")
    print(f"Incident Summary: {summary['summary']}")
    print(f"Severity: {summary.get('severity_assessment', 'N/A')}")
    print(f"Total errors: {summary['error_count']}")
