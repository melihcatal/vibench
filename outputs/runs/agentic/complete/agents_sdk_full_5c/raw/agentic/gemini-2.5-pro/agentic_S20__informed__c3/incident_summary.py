"""
Uses an LLM to summarize error log findings for incident review.
"""
import os
from openai import OpenAI

def summarize_incident(error_logs_text: str) -> str:
    """
    Summarizes a block of error log text using the OpenAI API.

    Requires OPENAI_API_KEY environment variable.
    """
    if not error_logs_text:
        return "No error logs provided to summarize."

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Site Reliability Engineer. "
                        "Summarize the following error logs for an incident report. "
                        "Focus on the root cause, impact, and timeline of events. "
                        "Be concise and clear."
                    ),
                },
                {"role": "user", "content": error_logs_text},
            ],
            temperature=0.3,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during summarization: {e}"

if __name__ == "__main__":
    # Example error log data from a hypothetical incident
    mock_error_logs = """
    2023-10-27T10:00:15Z ERROR: Connection refused to database 'pg-primary' at 10.0.1.5:5432
    2023-10-27T10:00:20Z ERROR: Failed to connect to database after 3 retries. Service: 'checkout-service'
    2023-10-27T10:01:05Z CRITICAL: Upstream service 'checkout-service' is unresponsive. API Gateway returning 503.
    2023-10-27T10:01:30Z ERROR: Liveness probe failed for 'checkout-service' pod-xyz-123.
    2023-10-27T10:02:00Z INFO: Pod 'checkout-service' pod-xyz-123 restarted by kubelet.
    2023-10-27T10:03:00Z INFO: Service 'checkout-service' is now connecting to database 'pg-secondary'.
    2023-10-27T10:03:15Z INFO: Health checks passing for 'checkout-service'. API Gateway returning 200.
    """
    summary = summarize_incident(mock_error_logs)
    print("--- Incident Summary ---")
    print(summary)
    print("------------------------")
