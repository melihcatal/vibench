from openai import OpenAI
import os
from typing import List, Dict

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def incident_summary(error_logs: List[Dict]) -> str:
    """
    Summarizes error-log findings for incident review using OpenAI's GPT model.

    Args:
        error_logs (List[Dict]): List of error log entries.

    Returns:
        str: A summary of the incident findings.
    """
    if not error_logs:
        return "No error logs provided."

    # Prepare the prompt
    prompt = (
        "Summarize the following error logs for an incident review. "
        "Focus on identifying the root cause, affected components, and potential impact.\n\n"
        f"Error Logs: {error_logs}"
    )

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an incident response assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
