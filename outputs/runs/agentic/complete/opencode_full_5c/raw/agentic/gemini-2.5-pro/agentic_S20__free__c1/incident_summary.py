import json
from query_error_logs import query_error_logs
from observability_client import get_generative_model_client


def summarize_incidents(log_name: str, hours_ago: int = 24) -> str:
    """Summarizes error logs for incident review using a generative model."""
    error_logs = query_error_logs(log_name, hours_ago)
    if not error_logs:
        return "No error incidents found in the specified time range."

    model = get_generative_model_client(model_name="gemini-1.5-flash")

    prompt = f"""
    The following is a list of error logs from our system. 
    Please provide a concise summary for an incident report.
    Focus on the unique error messages, frequency, and potential root cause if evident.

    Error Logs:
    {json.dumps(error_logs, indent=2)}
    """

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    summary = summarize_incidents("my-structured-log", hours_ago=24)
    print("--- Incident Summary ---")
    print(summary)
    print("------------------------")
