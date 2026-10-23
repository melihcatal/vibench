from typing import List, Dict
from openai import OpenAI
import os


class IncidentSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize_errors(self, error_logs: List[Dict[str, str]]) -> str:
        log_texts = "\n".join([f"{log.get('timestamp')}: {log.get('message')}" for log in error_logs])
        prompt = (
            "Summarize the following error logs into a concise incident report:\n"
            f"{log_texts}\n\n"
            "Summary:"
        )
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    summarizer = IncidentSummarizer()
    sample_errors = [
        {"timestamp": "2023-10-01T12:00:00Z", "message": "Database connection failed"},
        {"timestamp": "2023-10-01T12:01:00Z", "message": "API timeout error"},
    ]
    print(summarizer.summarize_errors(sample_errors))