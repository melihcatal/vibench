import os
from openai import OpenAI
from datetime import datetime, timedelta
from google.cloud import logging
from typing import List
from observability_client import get_google_cloud_project
from observability_models import LogQuery

def get_recent_error_logs(hours_back: int = 24) -> List[str]:
    project = get_google_cloud_project()
    client = logging.Client(project=project)
    now = datetime.utcnow()
    start = now - timedelta(hours=hours_back)
    query = LogQuery(filter_str='severity >= "ERROR"', start_time=start, page_size=20)
    filter_str = query.build_filter()
    entries_it = client.list_entries(filter_=filter_str, order_by="TIMESTAMP")
    entries = list(entries_it)
    return [str(entry.payload.get('message', entry.text_payload or '')) for entry in entries[:20]]

def incident_summary(hours_back: int = 24) -> str:
    error_messages = get_recent_error_logs(hours_back)
    if not error_messages:
        return "No recent errors found."
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize the key issues from these recent error log messages for incident review. "
        "Focus on common patterns, affected services, and potential root causes:\\n\\n" +
        '\\n'.join(error_messages)
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
