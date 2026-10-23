import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import Counter
import openai
from openai import OpenAI

from observability_models import LogEvent, LogLevel, IncidentSummary
from query_error_logs import query_error_logs


def summarize_incident(hours: int = 24, incident_id: str = None) -> IncidentSummary:
    """
    Summarize error-log findings for incident review using OpenAI GPT.

    Args:
        hours: Hours to analyze
        incident_id: Optional incident ID (generated if not provided)

    Returns:
        IncidentSummary with analysis
    """
    if incident_id is None:
        incident_id = f"incident-{uuid.uuid4().hex[:8]}"

    print(f"Analyzing incident {incident_id} for past {hours} hours...")

    result = query_error_logs(hours=hours, limit=500)

    if not result.results:
        print(f"No error logs found for incident {incident_id}")
        return IncidentSummary(
            incident_id=incident_id,
            start_time=datetime.utcnow() - timedelta(hours=hours),
            end_time=datetime.utcnow(),
            error_count=0,
            unique_services=[],
            most_common_errors=[],
            correlation_ids=[],
        )

    error_logs = result.results
    timestamps = [log.timestamp for log in error_logs if log.timestamp]

    start_time = (
        min(timestamps) if timestamps else datetime.utcnow() - timedelta(hours=hours)
    )
    end_time = max(timestamps) if timestamps else datetime.utcnow()

    services = set()
    correlation_ids = set()
    error_messages = []

    for log in error_logs:
        if log.service:
            services.add(log.service)
        if log.correlation_id:
            correlation_ids.add(log.correlation_id)
        error_messages.append(log.message)

    message_counter = Counter(error_messages)
    most_common = [
        {"message": msg, "count": count}
        for msg, count in message_counter.most_common(10)
    ]

    summary = IncidentSummary(
        incident_id=incident_id,
        start_time=start_time,
        end_time=end_time,
        error_count=len(error_logs),
        unique_services=list(services),
        most_common_errors=most_common,
        correlation_ids=list(correlation_ids)[:20],
    )

    try:
        openai_client = OpenAI(
            api_key=openai.api_key if hasattr(openai, "api_key") else None
        )

        log_samples = "\n".join([f"- {log.message}" for log in error_logs[:10]])

        prompt = f"""
        Analyze these application error logs from an incident and provide a summary for review:
        
        Incident ID: {incident_id}
        Time Range: {start_time} to {end_time}
        Total Errors: {len(error_logs)}
        Affected Services: {", ".join(services)}
        
        Sample Error Messages:
        {log_samples}
        
        Please provide:
        1. A brief summary of what happened
        2. The most likely root cause based on error patterns
        3. Recommended next steps for investigation
        4. Severity assessment (Low/Medium/High/Critical)
        """

        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced SRE analyzing application error logs for incident review.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        ai_summary = response.choices[0].message.content
        print(f"OpenAI GPT-4 generated incident summary for {incident_id}")
        print("=" * 60)
        print(ai_summary)
        print("=" * 60)

        summary.ai_analysis = ai_summary

    except Exception as e:
        print(f"Note: Could not generate AI summary: {e}")
        summary.ai_analysis = None

    print(f"Incident {incident_id} analysis complete:")
    print(f"- {summary.error_count} total errors")
    print(f"- {len(summary.unique_services)} affected services")
    print(f"- {len(summary.correlation_ids)} unique correlation IDs")
    print(f"- Time range: {summary.start_time} to {summary.end_time}")

    return summary


def generate_incident_report(incident_id: str, hours: int = 24) -> Dict[str, Any]:
    """
    Generate a comprehensive incident report.

    Args:
        incident_id: Incident identifier
        hours: Hours to analyze

    Returns:
        Dictionary with incident report
    """
    summary = summarize_incident(hours=hours, incident_id=incident_id)

    report = summary.to_report_dict()

    if hasattr(summary, "ai_analysis") and summary.ai_analysis:
        report["ai_analysis"] = summary.ai_analysis

    report["analysis_timestamp"] = datetime.utcnow().isoformat()
    report["time_window_hours"] = hours

    severity_score = calculate_incident_severity(summary)
    report["severity_score"] = severity_score
    report["severity_level"] = map_severity_level(severity_score)

    return report


def calculate_incident_severity(summary: IncidentSummary) -> float:
    """
    Calculate a severity score for the incident.

    Args:
        summary: IncidentSummary

    Returns:
        Severity score (0-100)
    """
    score = 0.0

    error_count = summary.error_count
    if error_count > 100:
        score += 40
    elif error_count > 50:
        score += 30
    elif error_count > 20:
        score += 20
    elif error_count > 5:
        score += 10

    service_count = len(summary.unique_services)
    if service_count > 3:
        score += 30
    elif service_count > 1:
        score += 20
    elif service_count == 1:
        score += 10

    duration_hours = (summary.end_time - summary.start_time).total_seconds() / 3600
    if duration_hours > 4:
        score += 30
    elif duration_hours > 1:
        score += 20
    elif duration_hours > 0.25:
        score += 10

    return min(score, 100)


def map_severity_level(score: float) -> str:
    """
    Map severity score to level.

    Args:
        score: Severity score (0-100)

    Returns:
        Severity level string
    """
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    elif score >= 20:
        return "Low"
    else:
        return "Informational"


def compare_incidents(incident_ids: List[str], hours: int = 24) -> Dict[str, Any]:
    """
    Compare multiple incidents.

    Args:
        incident_ids: List of incident IDs to compare
        hours: Hours to analyze for each

    Returns:
        Dictionary with comparison results
    """
    incidents = {}

    for incident_id in incident_ids:
        print(f"Analyzing incident: {incident_id}")
        summary = summarize_incident(hours=hours, incident_id=incident_id)
        incidents[incident_id] = summary

    comparison = {
        "incident_count": len(incident_ids),
        "incidents": {},
        "statistics": {
            "total_errors": sum(i.error_count for i in incidents.values()),
            "unique_services": len(
                set().union(*[set(i.unique_services) for i in incidents.values()])
            ),
            "avg_errors_per_incident": sum(i.error_count for i in incidents.values())
            / len(incidents)
            if incidents
            else 0,
        },
    }

    for incident_id, summary in incidents.items():
        comparison["incidents"][incident_id] = {
            "error_count": summary.error_count,
            "services": summary.unique_services,
            "severity": map_severity_level(calculate_incident_severity(summary)),
            "time_range": f"{summary.start_time} to {summary.end_time}",
        }

    return comparison
