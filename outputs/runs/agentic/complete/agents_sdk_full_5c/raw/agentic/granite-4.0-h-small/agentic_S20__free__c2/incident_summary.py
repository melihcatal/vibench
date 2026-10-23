import json
from typing import List, Dict
from observability_models import ErrorMessage, IncidentData
from observability_client import post_process_response

def summarize_incident(messages: List[ErrorMessage]) -> IncidentData:
    """Summarize error-log findings for incident review.
    Produces a concise structure that can be consumed by incident management systems.
    """
    correlation_ids = list({msg["correlation_id"] for msg in messages})
    error_messages = messages  # already in required format
    summary = "Multiple error logs observed. Details:",
    # Example short summary; in real cases apply aggregation logic
    details = json.dumps([msg for msg in messages], indent=2)
    return {
        "incident_id": "INC-20230815-001",
        "correlation_ids": correlation_ids,
        "error_messages": error_messages,
        "summary": summary[0] + \"\n\" + details
    }

# Example usage (will be removed in production)
if __name__ == "__main__":
    # Simulate fetched errors
    fetched = [
        {"correlation_id": "req-001", "severity": "error", "message": "DB timeout", "timestamp": 1723732800},
        {"correlation_id": "req-001", "severity": "error", "message": "Cache miss", "timestamp": 1723732820},
        {"correlation_id": "req-002", "severity": "error", "message": "File not found", "timestamp": 1723732850}
    ]
    incident = summarize_incident(fetched)
    print("Incident summary:", incident)
    # In production this would be sent to an incident tracking API.
