import os
from typing import List

from observability_client import get_gemini_model


def summarize_incident_logs(log_messages: List[str]) -> str:
    model = get_gemini_model("gemini-pro")  # Using gemini-pro for text summarization

    if not log_messages:
        return "No log messages provided for summarization."

    # Combine log messages into a single string for summarization
    combined_logs = "\n".join(log_messages)

    prompt = (
        "Summarize the following log entries for an incident review. "
        "Focus on key errors, their potential causes, and impact:\n\n"
        f"{combined_logs}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing logs: {e}"
