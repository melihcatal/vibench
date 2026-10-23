import os
import google.generativeai as genai


def summarize_incident(error_logs: list[str]) -> str:
    """
    Summarizes a list of error log messages for an incident review
    using the Google Gemini API.

    Args:
        error_logs: A list of error log message strings.

    Returns:
        A string containing the summary of the incident.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        "You are an expert Site Reliability Engineer. "
        "Based on the following list of error log messages from a production incident, "
        "please provide a concise summary of the likely root cause, impact, and "
        "suggested next steps for investigation. Format the output clearly.\n\n"
        "Error Logs:\n"
        "------------\n"
    )

    for log in error_logs:
        prompt += f"- {log}\n"

    response = model.generate_content(prompt)

    return response.text


if __name__ == "__main__":
    if os.environ.get("GOOGLE_API_KEY"):
        sample_errors = [
            "FATAL: Connection to database 'user_db_prod' on host 'db-prod-1.region.gcp' failed: timeout expired",
            "ERROR: Upstream service 'auth-service' returned 503 Service Unavailable",
            "CRITICAL: Failed to acquire lock on resource 'payment_processing'. The operation will be retried.",
            "FATAL: Connection to database 'user_db_prod' on host 'db-prod-1.region.gcp' failed: timeout expired",
        ]
        summary = summarize_incident(sample_errors)
        print("--- Incident Summary ---")
        print(summary)
    else:
        print("GOOGLE_API_KEY not set. Skipping example run.")
