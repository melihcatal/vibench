import os
import json
from typing import List, Dict, Any
import anthropic


def summarize_error_logs_for_incident(
    error_logs: List[Dict[str, Any]], incident_context: str = ""
) -> Dict[str, Any]:
    """Summarize error-log findings for incident review using Anthropic Claude."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    # Prepare log data for analysis
    log_summary = {
        "total_errors": len(error_logs),
        "services_affected": set(),
        "severity_counts": {},
        "sample_messages": [],
    }

    for log in error_logs[:10]:  # Take first 10 for context
        log_summary["services_affected"].add(log.get("service", "unknown"))
        severity = log.get("severity", "ERROR")
        log_summary["severity_counts"][severity] = (
            log_summary["severity_counts"].get(severity, 0) + 1
        )
        log_summary["sample_messages"].append(log.get("message", ""))

    log_summary["services_affected"] = list(log_summary["services_affected"])

    # Create prompt for Claude
    prompt = f"""You are analyzing error logs for an incident review. Here is the context:
{incident_context}

Error Log Summary:
- Total errors: {log_summary["total_errors"]}
- Services affected: {", ".join(log_summary["services_affected"])}
- Severity distribution: {json.dumps(log_summary["severity_counts"])}
- Sample error messages: {json.dumps(log_summary["sample_messages"][:3])}

Please provide a concise incident summary including:
1. Root cause analysis (based on error patterns)
2. Impact assessment (services affected, severity)
3. Recommended immediate actions
4. Suggested follow-up investigations

Format the response as a JSON object with these keys: root_cause, impact, immediate_actions, follow_up_investigations.
Each value should be a string or array of strings."""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.1,
            system="You are a senior SRE analyzing error logs for incident response. Provide clear, actionable insights.",
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse the response
        content = response.content[0].text

        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                summary = json.loads(json_str)
            else:
                # If no JSON found, create structured response from text
                summary = {
                    "root_cause": "Unable to parse specific root cause from logs",
                    "impact": f"{log_summary['total_errors']} errors across {len(log_summary['services_affected'])} services",
                    "immediate_actions": [
                        "Review error patterns",
                        "Check service health",
                    ],
                    "follow_up_investigations": [
                        "Analyze error trends",
                        "Review recent deployments",
                    ],
                    "raw_response": content,
                }
        except json.JSONDecodeError:
            summary = {
                "root_cause": "Error log analysis completed",
                "impact": f"{log_summary['total_errors']} errors detected",
                "immediate_actions": ["Review the error logs manually"],
                "follow_up_investigations": ["Conduct deeper analysis"],
                "raw_response": content,
            }

        # Add metadata
        summary["metadata"] = {
            "model_used": "claude-3-sonnet-20240229",
            "total_errors_analyzed": log_summary["total_errors"],
            "services_affected": log_summary["services_affected"],
            "analysis_timestamp": os.getenv("ANALYSIS_TIMESTAMP", ""),
        }

        print(
            f"Incident summary generated using Anthropic Claude for {log_summary['total_errors']} error logs"
        )
        return summary

    except Exception as e:
        print(f"Error calling Anthropic API: {e}")
        raise
