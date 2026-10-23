import os
import json
from typing import List, Dict, Any
from anthropic import Anthropic


def summarize_error_logs_for_incident(
    error_logs: List[Dict[str, Any]], incident_context: str = ""
) -> Dict[str, Any]:
    """Summarize error-log findings for incident review using Anthropic Claude."""

    # Initialize Anthropic client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    # Prepare log data for summarization
    log_summaries = []
    for i, log in enumerate(error_logs[:20]):  # Limit to 20 logs for context
        summary = {
            "index": i + 1,
            "timestamp": log.get("timestamp", "unknown"),
            "severity": log.get("severity", "unknown"),
            "service": log.get(
                "service_name", log.get("resource_labels", {}).get("service", "unknown")
            ),
            "message": log.get("message", str(log.get("payload", "No message")))[:200],
        }
        log_summaries.append(summary)

    # Count by severity
    severity_counts = {}
    for log in error_logs:
        severity = log.get("severity", "UNKNOWN")
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    # Count by service
    service_counts = {}
    for log in error_logs:
        service = log.get(
            "service_name", log.get("resource_labels", {}).get("service", "unknown")
        )
        service_counts[service] = service_counts.get(service, 0) + 1

    # Prepare prompt for Claude
    prompt = f"""You are an incident response engineer analyzing error logs. 
Provide a concise incident summary based on the following error logs.

Incident Context: {incident_context if incident_context else "General error log analysis"}

Error Log Statistics:
- Total errors: {len(error_logs)}
- Severity distribution: {json.dumps(severity_counts, indent=2)}
- Service distribution: {json.dumps(service_counts, indent=2)}

Recent Error Logs (up to 20):
{json.dumps(log_summaries, indent=2)}

Please provide:
1. A brief executive summary of the incident
2. Key patterns or commonalities in the errors
3. Most affected services/components
4. Recommended immediate actions
5. Suggested follow-up investigations

Format the response as a structured JSON with these fields:
- executive_summary
- key_patterns
- affected_services
- immediate_actions
- follow_up_investigations
"""

    try:
        # Call Anthropic Claude
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.2,
            system="You are a helpful incident response assistant specializing in log analysis and system diagnostics.",
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse the response
        summary_text = response.content[0].text

        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            json_start = summary_text.find("{")
            json_end = summary_text.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = summary_text[json_start:json_end]
                summary_data = json.loads(json_str)
            else:
                # If no JSON found, create a structured response from the text
                summary_data = {
                    "executive_summary": summary_text[:500],
                    "key_patterns": "Extracted from analysis",
                    "affected_services": list(service_counts.keys()),
                    "immediate_actions": [
                        "Review logs for root cause",
                        "Check service health",
                    ],
                    "follow_up_investigations": [
                        "Analyze error patterns",
                        "Review recent deployments",
                    ],
                }
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            summary_data = {
                "executive_summary": summary_text[:500],
                "key_patterns": "Unable to parse detailed patterns",
                "affected_services": list(service_counts.keys()),
                "immediate_actions": ["Review the error logs manually"],
                "follow_up_investigations": ["Complete manual analysis"],
            }

        # Add metadata
        result = {
            "incident_summary": summary_data,
            "metadata": {
                "total_errors_analyzed": len(error_logs),
                "severity_distribution": severity_counts,
                "service_distribution": service_counts,
                "model_used": "claude-3-sonnet-20240229",
                "provider": "Anthropic",
            },
        }

        return result

    except Exception as e:
        # Fallback summary if API call fails
        return {
            "incident_summary": {
                "executive_summary": f"Error analyzing {len(error_logs)} logs: {str(e)}",
                "key_patterns": ["Analysis failed"],
                "affected_services": list(service_counts.keys()),
                "immediate_actions": ["Check API connectivity", "Review logs manually"],
                "follow_up_investigations": ["Fix summarization service"],
            },
            "metadata": {
                "total_errors_analyzed": len(error_logs),
                "severity_distribution": severity_counts,
                "service_distribution": service_counts,
                "error": str(e),
            },
        }


if __name__ == "__main__":
    # Example usage
    sample_logs = [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "severity": "ERROR",
            "service_name": "api-gateway",
            "message": "Connection timeout to user-service",
            "resource_labels": {"service": "api-gateway"},
        },
        {
            "timestamp": "2024-01-15T10:31:00Z",
            "severity": "ERROR",
            "service_name": "user-service",
            "message": "Database connection pool exhausted",
            "resource_labels": {"service": "user-service"},
        },
    ]

    result = summarize_error_logs_for_incident(
        error_logs=sample_logs,
        incident_context="Service connectivity issues starting at 10:30 UTC",
    )
    print("Incident Summary:")
    print(json.dumps(result, indent=2))
