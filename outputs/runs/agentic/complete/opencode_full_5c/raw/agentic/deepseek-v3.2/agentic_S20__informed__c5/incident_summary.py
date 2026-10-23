import os
from typing import List, Dict, Any
from datetime import datetime
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING
import google.generativeai as genai


def summarize_error_logs(service_name: str, hours_back: int = 24) -> str:
    """Summarize error-log findings for incident review using Google Gemini API."""
    client = logging.Client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    filter_str = f"severity >= ERROR"
    filter_str += f' AND jsonPayload.service = "{service_name}"'
    filter_str += f' AND timestamp >= "{start_time.isoformat()}Z"'
    filter_str += f' AND timestamp <= "{end_time.isoformat()}Z"'

    entries = client.list_entries(
        filter_=filter_str, order_by=DESCENDING, page_size=100
    )

    error_logs = []
    for entry in entries:
        error_logs.append(
            {
                "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
                "severity": entry.severity,
                "message": entry.payload.get("message")
                if isinstance(entry.payload, dict)
                else str(entry.payload),
                "component": entry.payload.get("component")
                if isinstance(entry.payload, dict)
                else None,
                "error_code": entry.payload.get("error_code")
                if isinstance(entry.payload, dict)
                else None,
            }
        )

    if not error_logs:
        return "No error logs found in the specified time range."

    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-1.5-pro")

    log_summary_text = (
        f"Error logs for service '{service_name}' from {start_time} to {end_time}:\n\n"
    )
    for i, log in enumerate(error_logs[:20]):
        log_summary_text += (
            f"{i + 1}. [{log['timestamp']}] {log['severity']}: {log['message']}"
        )
        if log.get("component"):
            log_summary_text += f" (Component: {log['component']})"
        if log.get("error_code"):
            log_summary_text += f" (Error Code: {log['error_code']})"
        log_summary_text += "\n"

    if len(error_logs) > 20:
        log_summary_text += f"\n... and {len(error_logs) - 20} more errors\n"

    prompt = f"""Analyze these error logs and provide an incident summary for the engineering team.

{log_summary_text}

Please provide a concise incident summary including:
1. Overall severity assessment (Low/Medium/High/Critical)
2. Main error patterns or categories
3. Most affected components
4. Time distribution of errors
5. Recommended immediate actions
6. Suggested investigation steps

Format the response clearly with sections and bullet points where appropriate."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary with Gemini API: {str(e)}"


if __name__ == "__main__":
    summary = summarize_error_logs(service_name="my-application", hours_back=6)
    print("=== INCIDENT SUMMARY ===")
    print(summary)
