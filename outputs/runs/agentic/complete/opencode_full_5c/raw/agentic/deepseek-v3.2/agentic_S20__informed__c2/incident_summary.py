import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from query_error_logs import query_error_logs


def summarize_error_logs_for_incident(
    hours_back: int = 24,
    severity: str = "ERROR",
    component: str = None,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Summarize error-log findings for incident review using OpenAI GPT.

    Args:
        hours_back: Number of hours to look back
        severity: Log severity to filter by
        component: Optional component name to filter by
        model: OpenAI model to use (gpt-4o, gpt-4-turbo, etc.)

    Returns:
        Dictionary with incident summary
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = OpenAI(api_key=api_key)

    error_logs = query_error_logs(
        hours_back=hours_back, severity=severity, component=component, limit=50
    )

    if not error_logs:
        return {
            "summary": "No error logs found for the specified time period.",
            "total_errors": 0,
            "time_range_hours": hours_back,
        }

    log_messages = []
    severity_counts = {}
    component_counts = {}

    for log in error_logs:
        log_messages.append(f"[{log.severity}] {log.timestamp}: {log.message}")

        severity_counts[log.severity] = severity_counts.get(log.severity, 0) + 1

        component_name = log.labels.get("component", "unknown")
        component_counts[component_name] = component_counts.get(component_name, 0) + 1

    logs_text = "\n".join(log_messages[:20])

    prompt = f"""You are an incident response analyst reviewing error logs from a production system.

Error Logs (last {hours_back} hours, severity: {severity}):
{logs_text}

Please provide a concise incident summary including:
1. Main issue or pattern observed
2. Most affected component(s)
3. Timeline of when errors started/peaked
4. Suggested immediate actions
5. Recommended follow-up investigation areas

Format the response as a structured JSON with these fields:
- summary: Brief overall summary
- primary_issue: Main problem identified
- affected_components: List of components with error counts
- timeline_analysis: Analysis of error timing
- immediate_actions: List of recommended immediate actions
- investigation_areas: List of areas for further investigation
- confidence_level: Low/Medium/High based on log clarity
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful incident response analyst.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        summary_data = json.loads(response.choices[0].message.content)

        result = {
            "summary": summary_data,
            "total_errors": len(error_logs),
            "severity_distribution": severity_counts,
            "component_distribution": component_counts,
            "time_range_hours": hours_back,
            "model_used": model,
            "sample_logs": log_messages[:5],
        }

        print(f"Incident summary generated using OpenAI {model}")
        print(f"Total errors analyzed: {len(error_logs)}")
        print(f"Summary: {summary_data.get('summary', 'No summary provided')[:200]}...")

        return result

    except Exception as e:
        print(f"Error generating incident summary with OpenAI: {e}")

        fallback_summary = {
            "summary": f"Found {len(error_logs)} error logs in the last {hours_back} hours.",
            "primary_issue": "Multiple errors detected - manual review required",
            "affected_components": list(component_counts.keys()),
            "timeline_analysis": "Errors distributed throughout time period",
            "immediate_actions": [
                "Review error logs manually",
                "Check system health metrics",
            ],
            "investigation_areas": [
                "Root cause analysis",
                "Error pattern identification",
            ],
            "confidence_level": "Low",
        }

        return {
            "summary": fallback_summary,
            "total_errors": len(error_logs),
            "severity_distribution": severity_counts,
            "component_distribution": component_counts,
            "time_range_hours": hours_back,
            "model_used": "fallback",
            "error": str(e),
        }


def generate_incident_report(
    error_logs_data: List[Dict[str, Any]], model: str = "gpt-4o"
) -> str:
    """
    Generate a detailed incident report from error log data using OpenAI GPT.

    Args:
        error_logs_data: List of error log dictionaries
        model: OpenAI model to use

    Returns:
        Markdown formatted incident report
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = OpenAI(api_key=api_key)

    logs_text = json.dumps(error_logs_data[:15], indent=2)

    prompt = f"""Generate a comprehensive incident report based on the following error logs:

Error Logs Data:
{logs_text}

Create a professional incident report in markdown format with these sections:
1. Executive Summary
2. Incident Timeline
3. Impact Assessment
4. Root Cause Analysis
5. Resolution Actions Taken
6. Recommendations for Prevention
7. Lessons Learned

Include specific references to the log data where appropriate.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an experienced incident response manager.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    report = response.choices[0].message.content
    print(f"Incident report generated using OpenAI {model}")
    return report


if __name__ == "__main__":
    summary = summarize_error_logs_for_incident(
        hours_back=1, severity="ERROR", model="gpt-4o-mini"
    )

    print(f"\nIncident Summary from OpenAI GPT:")
    print(f"Total errors: {summary['total_errors']}")
    if "summary" in summary and isinstance(summary["summary"], dict):
        print(f"Primary issue: {summary['summary'].get('primary_issue', 'N/A')}")
        print(f"Confidence: {summary['summary'].get('confidence_level', 'N/A')}")
