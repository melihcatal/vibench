import os
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
from anthropic import Anthropic
from observability_models import LogEntry, IncidentSummary, LogSeverity
from observability_client import ObservabilityClient


def summarize_error_logs_for_incident(
    project_id: str, log_name: str, hours_back: int = 24
) -> Dict[str, Any]:
    """Summarize error-log findings for incident review using Anthropic Claude."""
    client = ObservabilityClient(project_id)

    error_logs = client.get_error_logs(log_name, hours_back=hours_back)

    if not error_logs:
        return {"error": "No error logs found in the specified time range"}

    incident_id = f"incident_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    timestamps = [log["timestamp"] for log in error_logs if log.get("timestamp")]
    start_time = (
        min(timestamps)
        if timestamps
        else datetime.utcnow() - timedelta(hours=hours_back)
    )
    end_time = max(timestamps) if timestamps else datetime.utcnow()

    components = set()
    error_messages = []

    for log in error_logs[:10]:
        payload = log.get("payload", {})
        if isinstance(payload, dict):
            component = payload.get("component")
            if component:
                components.add(component)

            message = payload.get("message", str(payload))
            error_messages.append(
                {
                    "message": message[:200],
                    "severity": log.get("severity"),
                    "timestamp": log.get("timestamp"),
                    "component": component,
                }
            )

    anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    sample_errors_text = "\n".join(
        [
            f"- {err['message']} (severity: {err['severity']}, component: {err['component']})"
            for err in error_messages[:5]
        ]
    )

    prompt = f"""You are an incident response analyst. Summarize the following error logs for an incident review.

Time range: {start_time} to {end_time}
Total error count: {len(error_logs)}
Affected components: {", ".join(sorted(components))}

Sample errors:
{sample_errors_text}

Please provide a concise incident summary including:
1. Brief description of the issue
2. Most likely root cause based on error patterns
3. Recommended immediate actions
4. Components requiring investigation

Format the response as JSON with keys: summary, root_cause_hypothesis, immediate_actions, investigation_targets."""

    try:
        response = anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        try:
            summary_data = json.loads(summary_text)
        except json.JSONDecodeError:
            summary_data = {"analysis": summary_text}

        incident_summary = IncidentSummary(
            incident_id=incident_id,
            start_time=start_time,
            end_time=end_time,
            error_count=len(error_logs),
            affected_components=list(components),
            most_common_error=error_messages[0]["message"] if error_messages else None,
            sample_errors=error_messages[:5],
        )

        result = {
            "incident_summary": incident_summary.to_report(),
            "ai_analysis": summary_data,
            "total_errors": len(error_logs),
            "time_range": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
            },
        }

        print(f"Incident summary generated: {incident_id}")
        print(f"Total errors analyzed: {len(error_logs)}")
        print(f"Affected components: {', '.join(sorted(components))}")

        return result

    except Exception as e:
        print(f"Error generating incident summary: {e}")

        incident_summary = IncidentSummary(
            incident_id=incident_id,
            start_time=start_time,
            end_time=end_time,
            error_count=len(error_logs),
            affected_components=list(components),
            sample_errors=error_messages[:3],
        )

        return {"incident_summary": incident_summary.to_report(), "error": str(e)}


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    log_name = "application-logs"

    summary = summarize_error_logs_for_incident(project_id, log_name, hours_back=1)
    print(json.dumps(summary, indent=2, default=str))
