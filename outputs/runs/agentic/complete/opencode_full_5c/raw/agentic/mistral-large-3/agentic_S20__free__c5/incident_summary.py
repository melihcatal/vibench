from typing import List, Dict
from query_error_logs import query_error_logs
from observability_models import normalize_log_response


def summarize_error_logs_for_incident():
    """Summarize error logs for incident review using OpenAI's GPT-4."""
    error_logs = query_error_logs(severity="ERROR", hours=24)
    normalized_logs = [normalize_log_response(log) for log in error_logs]

    if not normalized_logs:
        return "No error logs found in the last 24 hours."

    log_texts = [
        f"Timestamp: {log['timestamp']}, Severity: {log['severity']}, Message: {log['message']}"
        for log in normalized_logs
    ]

    prompt = (
        "Summarize the following error logs for an incident review. "
        "Focus on identifying patterns, root causes, and potential impacts:\n\n"
        f"{'\\n'.join(log_texts)}"
    )

    # Use OpenAI's GPT-4 to generate the summary
    import openai

    openai.api_key = "sk-proj-..."  # Replace with actual OpenAI API key

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an incident response assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
    )

    return response.choices[0].message.content.strip()
