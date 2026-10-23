"""Summarize error-log findings for incident review using OpenAI GPT."""

import os
from typing import List

from openai import OpenAI
from observability_models import LogEntry


class IncidentSummarizer:
    """Summarize error logs using OpenAI GPT."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize_errors(self, log_entries: List[LogEntry]) -> str:
        """Summarize error logs for incident review."""
        if not log_entries:
            return "No error logs provided."
        
        log_texts = [
            f"{entry.timestamp} - {entry.severity} - {entry.message}"
            for entry in log_entries
        ]
        prompt = (
            "Summarize the following error logs for an incident review. "
            "Focus on root causes and potential impacts:\n\n"
            f"{'\\n'.join(log_texts)}"
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    from fetch_recent_logs import fetch_recent_logs
    
    logs = fetch_recent_logs(service="order-service", user_id="12345")
    error_logs = [log for log in logs if log.severity == "ERROR"]
    
    summarizer = IncidentSummarizer()
    summary = summarizer.summarize_errors(error_logs)
    print(summary)