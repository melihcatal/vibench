import os
import openai

def summarize_log_data(log_entries: list[str]) -> str:
    """
    Summarizes a list of log entries for an incident report using OpenAI.

    Args:
        log_entries: A list of log message strings.

    Returns:
        A string containing a summary of the incident.
    """
    if not log_entries:
        return "No log entries to summarize."

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    log_block = "\n".join(log_entries)
    
    prompt = f"""
    The following is a block of error logs from our production server.
    Please summarize these logs for an incident report.
    Identify the likely root cause, the user impact, and suggest immediate actions.

    Logs:
    ---
    {log_block}
    ---

    Summary:
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for summarizing technical logs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error communicating with OpenAI API: {e}"

if __name__ == '__main__':
    # Example error logs as if they were fetched from a logging service
    sample_errors = [
        "ERROR:root:Database connection failed: timeout expired",
        "ERROR:werkzeug:Exception on /api/v1/users [POST]",
        "CRITICAL:root:Service failed to start after 3 retries.",
        "ERROR:root:Database connection failed: timeout expired",
        "WARNING:root:High latency detected on user-service: 1500ms"
    ]
    summary = summarize_log_data(sample_errors)
    print("--- Incident Summary ---")
    print(summary)
