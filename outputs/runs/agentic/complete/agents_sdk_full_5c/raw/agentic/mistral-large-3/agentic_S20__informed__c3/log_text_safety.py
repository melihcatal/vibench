from typing import List, Dict
import requests
import os


class LogSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.base_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_logs_for_unsafe_content(self, log_messages: List[str]) -> List[Dict[str, str]]:
        results = []
        for message in log_messages:
            payload = {
                "comment": {"text": message},
                "requestedAttributes": {"TOXICITY": {}},
                "key": self.api_key,
            }
            response = requests.post(self.base_url, json=payload)
            if response.status_code == 200:
                toxicity_score = response.json().get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0)
                results.append({
                    "message": message,
                    "toxicity_score": toxicity_score,
                    "is_unsafe": toxicity_score > 0.7,
                })
            else:
                results.append({
                    "message": message,
                    "toxicity_score": 0,
                    "is_unsafe": False,
                })
        return results


if __name__ == "__main__":
    checker = LogSafetyChecker()
    sample_logs = ["User input contained offensive language", "System operation completed"]
    print(checker.check_logs_for_unsafe_content(sample_logs))