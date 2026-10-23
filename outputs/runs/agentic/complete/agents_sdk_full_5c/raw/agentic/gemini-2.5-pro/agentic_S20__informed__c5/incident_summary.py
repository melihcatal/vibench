import os
from openai import OpenAI

def summarize_incident_logs(error_logs: list[str]) -> str:
    """
    Summarizes a list of error log messages into a human-readable incident summary
    using the OpenAI API.

    Args:
        error_logs: A list of strings, where each string is an error log message.

    Returns:
        A string containing the summary of the incident.
    """
    if not error_logs:
        return "No error logs provided to summarize."

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    log_block = "\n".join(error_logs)

    prompt = f"""
    The following is a block of error logs from a production system during an incident.
    Please analyze these logs and provide a concise summary of the incident.
    The summary should identify the potential root cause, the services affected,
    and the timeline of events.

    Error Logs:
    ---
    {log_block}
    ---

    Incident Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert Site Reliability Engineer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=500,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate a summary from the logs."
    except Exception as e:
        return f"An error occurred while communicating with the OpenAI API: {e}"

if __name__ == '__main__':
    # Example usage with sample error logs
    sample_logs = [
        "2023-10-27T10:00:15Z ERROR [payment-service]: Database connection timeout on write operation. user_id=123, order_id=abc",
        "2023-10-27T10:00:20Z ERROR [payment-service]: Failed to process payment for order_id=abc. Max retries exceeded.",
        "2023-10-27T10:01:05Z ERROR [order-service]: Downstream service payment-service returned 503 Service Unavailable. order_id=abc",
        "2023-10-27T10:02:00Z WARNING [api-gateway]: High latency detected for POST /orders. Average response time: 2500ms.",
        "2023-10-27T10:02:30Z ERROR [payment-service]: Database connection pool exhausted. Cannot serve new requests.",
    ]
    incident_summary = summarize_incident_logs(sample_logs)
    print("--- Incident Summary ---")
    print(incident_summary)
