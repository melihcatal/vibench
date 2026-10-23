import json
from observability_client import observability_client
from observability_models import IncidentSummary

def summarize_error_logs_for_incident(error_logs: list[dict]) -> IncidentSummary:
    """
    Summarizes error-log findings for incident review using the Gemini API.

    Args:
        error_logs: A list of dictionaries, where each dictionary represents an error log entry.

    Returns:
        An IncidentSummary object.
    """
    model = observability_client.get_gemini_model("gemini-pro")

    log_data_str = json.dumps(error_logs, indent=2)

    prompt = f"""
    Analyze the following error logs to identify key issues, affected components, and suggest immediate actions.
    Provide a concise incident summary in JSON format with the following keys:
    - "title": A brief title for the incident.
    - "summary_text": A paragraph summarizing the incident, root causes, and impact.
    - "affected_components": A list of application components or services that appear to be affected.
    - "severity_score": An integer score from 1 (low) to 5 (critical) representing the incident severity.
    - "recommended_actions": A list of short, actionable steps for incident response.

    Error Logs:
    {log_data_str}

    JSON Summary:
    """

    response = model.generate_content(prompt)
    try:
        # Assuming the model reliably returns JSON in the first part of the text
        summary_json_str = response.text.strip()
        # Sometimes the model might include markdown code fences, try to strip them
        if summary_json_str.startswith("```json"):
            summary_json_str = summary_json_str[len("```json"):].strip()
        if summary_json_str.endswith("```"):
            summary_json_str = summary_json_str[:-len("```")].strip()

        summary_data = json.loads(summary_json_str)

        return IncidentSummary(
            title=summary_data.get("title", "Untitled Incident"),
            summary_text=summary_data.get("summary_text", "No summary provided."),
            affected_components=summary_data.get("affected_components", []),
            severity_score=summary_data.get("severity_score", 1),
            recommended_actions=summary_data.get("recommended_actions", []),
        )
    except json.JSONDecodeError as e:
        print(f"Error parsing Gemini response JSON: {e}")
        print(f"Raw response text: {response.text}")
        return IncidentSummary(
            title="Parsing Error Incident",
            summary_text=f"Failed to parse incident summary from Gemini. Raw response: {response.text}",
            affected_components=[],
            severity_score=1,
            recommended_actions=["Review raw logs manually.", "Check Gemini API response format."],
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return IncidentSummary(
            title="Unexpected Error Incident",
            summary_text=f"An unexpected error occurred during summary generation: {e}",
            affected_components=[],
            severity_score=1,
            recommended_actions=["Review logs manually."],
        )


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY environment variable is set
    # This example uses mock error logs, in a real scenario you would
    # retrieve them using query_error_logs.py
    sample_error_logs = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "severity": "ERROR",
            "component": "payment_service",
            "message": "Failed to process payment for user 123. Gateway timeout.",
            "trace_id": "abc-123"
        },
        {
            "timestamp": "2023-10-27T10:01:15Z",
            "severity": "ERROR",
            "component": "order_processing",
            "message": "Order 456 failed to create due to payment service error.",
            "trace_id": "abc-123"
        },
        {
            "timestamp": "2023-10-27T10:02:30Z",
            "severity": "WARNING",
            "component": "inventory_service",
            "message": "Low stock alert for item XYZ.",
            "trace_id": "def-456"
        }
    ]

    print("Generating incident summary from sample error logs...")
    summary = summarize_error_logs_for_incident(sample_error_logs)
    print("\n--- Incident Summary ---")
    print(f"Title: {summary.title}")
    print(f"Summary: {summary.summary_text}")
    print(f"Affected Components: {', '.join(summary.affected_components)}")
    print(f"Severity Score: {summary.severity_score}/5")
    print(f"Recommended Actions:")
    for action in summary.recommended_actions:
        print(f"- {action}")
