from openai import OpenAI
from typing import List, Dict


class IncidentSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize_error_logs(self, error_logs: List[Dict]) -> str:
        log_texts = [
            f"Timestamp: {log['timestamp']}, Severity: {log['severity']}, Message: {log['message']}, Details: {log['json_payload']}"
            for log in error_logs
        ]
        prompt = (
            "Summarize the following error logs into a concise incident report. "
            "Include key details like error patterns, affected components, and potential impact.\n\n"
            f"Logs:\n{chr(10).join(log_texts)}"
        )

        response = self.client.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    import os

    summarizer = IncidentSummarizer()
    sample_logs = [
        {
            "timestamp": "2023-01-01T00:00:00Z",
            "severity": "ERROR",
            "message": "Database connection failed",
            "json_payload": {"component": "database", "error_code": "500"},
        }
    ]
    print(summarizer.summarize_error_logs(sample_logs))
