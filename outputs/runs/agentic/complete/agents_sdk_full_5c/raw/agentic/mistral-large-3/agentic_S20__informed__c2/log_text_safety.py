"""Check selected log message text for unsafe content using Azure AI Content Safety."""

import os
from typing import List

import requests
from observability_models import LogEntry


class LogTextSafetyChecker:
    """Check log messages for unsafe content using Azure AI Content Safety."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety credentials not configured.")

    def check_text_safety(self, text: str) -> bool:
        """Check if text contains unsafe content."""
        url = f"{self.endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "categories": ["Hate", "Violence", "SelfHarm", "Sexual"],
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        for category in result.get("categoriesAnalysis", []):
            if category.get("severity", 0) > 2:
                return False
        return True

    def filter_unsafe_logs(self, log_entries: List[LogEntry]) -> List[LogEntry]:
        """Filter out logs with unsafe content."""
        safe_logs = []
        for entry in log_entries:
            if self.check_text_safety(entry.message):
                safe_logs.append(entry)
        return safe_logs


if __name__ == "__main__":
    from fetch_recent_logs import fetch_recent_logs
    
    logs = fetch_recent_logs(service="support-service", user_id="67890")
    checker = LogTextSafetyChecker()
    safe_logs = checker.filter_unsafe_logs(logs)
    
    for log in safe_logs:
        print(f"{log.timestamp} - {log.severity} - {log.message}")