import os
from openai import OpenAI
from typing import List
from observability_models import LogQueryResponse

def summarize_incident_logs(error_logs: List[LogQueryResponse]) -> str:
    """
    Summarizes a list of error logs into a human-readable incident summary
    using the OpenAI API.

    Args:
        error_logs: A list of LogQueryResponse objects.

    Returns:
        A string containing the incident summary.
    """
    if not error_logs:
        return "No error logs provided for summarization."

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    log_messages = "\n".join([f"- {log.timestamp.isoformat()}: {log.message}" for log in error_logs])

    prompt = f"""
    The following is a list of error log messages from a production system.
    Please analyze these logs and provide a concise incident summary.
    The summary should include:
    1. A brief, one-sentence overview of the primary issue.
    2. A potential root cause or the most affected service.
    3. The start time of the incident based on the logs.
    4. Key error messages or patterns observed.

    Log data:
    {log_messages}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert system reliability engineer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=500,
        )
        return response.choices[0].message.content or "Could not generate summary."
    except Exception as e:
        return f"Error communicating with OpenAI API: {e}"
