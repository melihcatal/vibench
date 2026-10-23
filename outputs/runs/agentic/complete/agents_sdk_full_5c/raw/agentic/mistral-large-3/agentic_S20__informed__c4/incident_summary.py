import os
from typing import List, Dict
from openai import OpenAI


class IncidentSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize_errors(self, error_logs: List[Dict]) -> str:
        log_texts = "\n".join([
            f"{log['timestamp']} - {log['severity']}: {log['message']}"
            for log in error_logs
        ])

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an incident response assistant. Summarize the following error logs."
                },
                {
                    "role": "user",
                    "content": f"Summarize these error logs:\n\n{log_texts}"
                }
            ],
            max_tokens=500
        )

        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    summarizer = IncidentSummarizer()
    sample_logs = [
        {"timestamp": "2023-01-01T00:00:00Z", "severity": "ERROR", "message": "Database connection failed"},
        {"timestamp": "2023-01-01T00:01:00Z", "severity": "CRITICAL", "message": "Service unavailable"}
    ]
    print(summarizer.summarize_errors(sample_logs))