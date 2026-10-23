import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_models import IncidentSummary, LogEntry


def summarize_error_logs(
    service_name: str, error_logs: List[LogEntry], hours_back: int = 24
) -> IncidentSummary:
    """
    Summarize error-log findings for incident review using OpenAI GPT.

    Args:
        service_name: Name of the service with errors
        error_logs: List of error log entries to summarize
        hours_back: Time window for the incident

    Returns:
        IncidentSummary with analysis and recommendations
    """
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        if not error_logs:
            return IncidentSummary(
                incident_id=str(uuid.uuid4()),
                service=service_name,
                start_time=datetime.utcnow().isoformat() + "Z",
                end_time=datetime.utcnow().isoformat() + "Z",
                error_count=0,
                unique_errors=[],
                affected_operations=[],
                severity="INFO",
                summary="No error logs found for analysis.",
            )

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours_back)

        unique_errors = []
        error_messages = []
        operations = set()

        for log in error_logs:
            if log.message not in unique_errors:
                unique_errors.append(log.message)
            error_messages.append(log.message)
            if log.operation:
                operations.add(log.operation)

        log_sample = "\n".join([f"- {msg}" for msg in error_messages[:10]])
        if len(error_messages) > 10:
            log_sample += f"\n... and {len(error_messages) - 10} more errors"

        prompt = f"""
        Analyze these error logs from service '{service_name}' over the past {hours_back} hours:
        
        {log_sample}
        
        Total errors: {len(error_logs)}
        Unique error patterns: {len(unique_errors)}
        
        Please provide:
        1. A brief summary of the incident
        2. The likely root cause category (e.g., network, database, authentication, configuration, code bug)
        3. Severity assessment (LOW, MEDIUM, HIGH, CRITICAL)
        4. Recommended immediate actions
        5. Suggested long-term fixes
        
        Format the response as a concise incident summary suitable for an engineering team.
        """

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced SRE (Site Reliability Engineer) analyzing error logs to create incident summaries.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        summary_text = response.choices[0].message.content

        severity = "MEDIUM"
        if "CRITICAL" in summary_text.upper():
            severity = "CRITICAL"
        elif "HIGH" in summary_text.upper():
            severity = "HIGH"
        elif "LOW" in summary_text.upper():
            severity = "LOW"

        incident_summary = IncidentSummary(
            incident_id=str(uuid.uuid4()),
            service=service_name,
            start_time=start_time.isoformat() + "Z",
            end_time=end_time.isoformat() + "Z",
            error_count=len(error_logs),
            unique_errors=unique_errors[:20],
            affected_operations=list(operations),
            severity=severity,
            summary=summary_text,
        )

        print(
            f"Generated incident summary using OpenAI GPT-4 for service: {service_name}"
        )
        print(f"Incident ID: {incident_summary.incident_id}")
        print(f"Severity: {incident_summary.severity}")

        return incident_summary

    except Exception as e:
        print(f"Failed to generate incident summary with OpenAI: {e}")

        fallback_summary = f"""
        Service: {service_name}
        Time window: {hours_back} hours
        Total errors: {len(error_logs)}
        Unique error patterns: {len(set([log.message for log in error_logs]))}
        
        Error analysis failed due to: {str(e)}
        
        Please review the raw error logs manually.
        """

        return IncidentSummary(
            incident_id=str(uuid.uuid4()),
            service=service_name,
            start_time=datetime.utcnow().isoformat() + "Z",
            end_time=datetime.utcnow().isoformat() + "Z",
            error_count=len(error_logs),
            unique_errors=[log.message for log in error_logs[:10]],
            affected_operations=list(
                set([log.operation for log in error_logs if log.operation])
            ),
            severity="UNKNOWN",
            summary=fallback_summary,
        )
