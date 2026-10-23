import os
import google.generativeai as genai
from typing import List


def summarize_incident_logs(logs: List[str]) -> str:
    """
    Summarizes a list of error log messages for an incident report using Gemini.

    Args:
        logs: A list of string-formatted log messages.

    Returns:
        A summary of the logs.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        "Summarize the following error log messages for a technical incident report. "
        "Focus on the root cause, impact, and timeline if possible:\n\n"
    )

    prompt += "\n".join(logs)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


if __name__ == "__main__":
    error_logs = [
        "ERROR: Database connection timeout on host db-prod-1. Retrying in 10s.",
        "ERROR: Failed to connect to database after 3 retries. Aborting transaction.",
        "CRITICAL: Service unavailable due to database connection failure.",
        "INFO: Attempting to failover to replica database db-replica-1.",
        "ERROR: Failover failed. Replica is not responding.",
    ]

    summary = summarize_incident_logs(error_logs)
    print("--- Incident Summary ---")
    print(summary)
