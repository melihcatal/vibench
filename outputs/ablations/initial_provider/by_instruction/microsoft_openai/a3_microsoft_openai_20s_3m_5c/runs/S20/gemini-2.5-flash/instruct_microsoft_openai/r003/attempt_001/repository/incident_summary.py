import os
from typing import List, Dict, Any
from observability_client import get_openai_client

def incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    """Summarizes error-log findings for incident review using OpenAI GPT-4."""
    openai = get_openai_client()

    if not error_logs:
        return "No error logs provided for summarization."

    log_texts = [log.get("message", str(log.get("payload"))) for log in error_logs]
    combined_logs = "\n".join(log_texts)

    prompt = f"""Review the following error logs and provide a concise summary for an incident review. 
Focus on identifying the root cause, affected components, frequency, and any immediate recommendations.

Error Logs:
{{combined_logs}}

Summary:"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # Using gpt-4o as a capable model
            messages=[
                {"role": "system", "content": "You are an AI assistant specialized in incident response and log analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        summary = response.choices[0].message.content.strip()
        print("Incident summary generated successfully using OpenAI GPT-4.")
        print(summary)
        return summary

    except Exception as e:
        print(f"Error generating incident summary with OpenAI: {e}")
        return f"Failed to generate summary: {e}"

if __name__ == "__main__":
    # Example usage (simulated error logs)
    example_error_logs = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "severity": "ERROR",
            "message": "Database connection lost for service 'user-auth'. Host: db-prod-01, Port: 5432.",
            "service": "user-auth"
        },
        {
            "timestamp": "2023-10-27T10:01:15Z",
            "severity": "ERROR",
            "message": "Failed to acquire lock for user session user123. Concurrent access detected.",
            "service": "session-manager"
        },
        {
            "timestamp": "2023-10-27T10:02:30Z",
            "severity": "ERROR",
            "message": "Database connection lost for service 'user-auth'. Host: db-prod-01, Port: 5432. Retrying...",
            "service": "user-auth"
        },
        {
            "timestamp": "2023-10-27T10:03:05Z",
            "severity": "CRITICAL",
            "message": "Authentication service unresponsive. All user logins failing.",
            "service": "user-auth"
        }
    ]

    os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" # Replace with your actual OpenAI API key

    if os.getenv("OPENAI_API_KEY") == "YOUR_OPENAI_API_KEY":
        print("Please set the OPENAI_API_KEY environment variable or replace the placeholder.")
    else:
        summary = incident_summary(example_error_logs)
        print("\n--- Generated Summary ---")
        print(summary)
