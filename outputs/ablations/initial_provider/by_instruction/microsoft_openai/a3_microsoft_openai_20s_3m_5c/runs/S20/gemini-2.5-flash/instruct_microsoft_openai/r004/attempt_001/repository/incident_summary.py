from typing import List
from observability_client import ObservabilityClient
from observability_models import LogEntry

def incident_summary(error_logs: List[LogEntry]) -> str:
    client = ObservabilityClient()
    openai_client = client.get_openai_client()

    if not openai_client:
        return "OpenAI client not configured. Cannot summarize incident."

    if not error_logs:
        return "No error logs provided for summarization."

    log_messages = [f"Severity: {log.severity}, Timestamp: {log.timestamp.isoformat()}, Message: {log.message}, Properties: {log.properties}" for log in error_logs]
    combined_logs_text = "\n".join(log_messages)

    prompt = f"""
    Review the following error log entries and provide a concise summary for an incident review. 
    Highlight key issues, potential root causes, and any recurring patterns. 

    Error Logs:
    {combined_logs_text}
    """

    try:
        chat_completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for higher quality
            messages=[
                {"role": "system", "content": "You are an incident response assistant. Summarize error logs clearly and concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        summary = chat_completion.choices[0].message.content.strip()
        print("Incident summary generated successfully.")
        return summary
    except Exception as e:
        return f"An error occurred during summarization with OpenAI: {e}"

if __name__ == "__main__":
    # Example usage (assuming you have some error logs from query_error_logs.py):
    from datetime import datetime, timedelta

    # Simulate some error logs
    sample_error_logs = [
        LogEntry(
            message="Database connection pool exhausted. Max connections reached.",
            severity="CRITICAL",
            timestamp=datetime.utcnow() - timedelta(minutes=5),
            properties={
                "component": "database_service",
                "error_code": 5001
            }
        ),
        LogEntry(
            message="Failed to process payment for user user456. Gateway timeout.",
            severity="ERROR",
            timestamp=datetime.utcnow() - timedelta(minutes=10),
            properties={
                "user_id": "user456",
                "service": "payment_gateway"
            }
        ),
        LogEntry(
            message="Database connection pool exhausted. Max connections reached.",
            severity="ERROR",
            timestamp=datetime.utcnow() - timedelta(minutes=7),
            properties={
                "component": "database_service",
                "error_code": 5001
            }
        ),
        LogEntry(
            message="Auth service responded with 401 Unauthorized for API call /users",
            severity="WARNING", # Even warnings can be relevant for incidents
            timestamp=datetime.utcnow() - timedelta(minutes=12),
            properties={
                "api_path": "/users",
                "status_code": 401
            }
        ),
    ]

    summary_report = incident_summary(sample_error_logs)
    print("\n--- Incident Summary Report ---")
    print(summary_report)
