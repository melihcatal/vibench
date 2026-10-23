from typing import List, Dict
import os
import google.generativeai as genai
from observability_client import GoogleLoggingClient
from observability_models import LogQuery
from datetime import datetime, timedelta


def summarize_incident_logs(severity: str = "ERROR", hours: int = 1) -> str:
    client = GoogleLoggingClient()
    time_from = datetime.utcnow() - timedelta(hours=hours)
    log_query = LogQuery(
        filter_severity=severity,
        time_from=time_from,
        custom_filters={"source": "application"},
    )
    response = client.query_logs(log_query)
    log_texts = [
        f"{entry['timestamp']} [{entry['severity']}] {entry['message']}"
        for entry in response.entries
    ]

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Summarize the following error logs for an incident review. "
        "Focus on root causes, impacted components, and suggested actions:\n\n"
        f"{chr(10).join(log_texts)}"
    )
    summary = model.generate_content(prompt)
    return summary.text