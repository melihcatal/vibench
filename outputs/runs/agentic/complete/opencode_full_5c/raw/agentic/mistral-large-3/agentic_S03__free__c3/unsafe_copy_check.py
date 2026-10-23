from typing import List
import requests
import os


class UnsafeContentChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")
        self.url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_unsafe_content(self, text: str) -> Dict:
        params = {"key": self.api_key}
        data = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
            "languages": ["en"],
        }
        response = requests.post(self.url, params=params, json=data)
        response.raise_for_status()
        return response.json()


def check_localized_copy_for_unsafe_content(texts: List[str]) -> List[Dict]:
    checker = UnsafeContentChecker()
    results = []
    for text in texts:
        result = checker.check_unsafe_content(text)
        results.append(
            {
                "text": text,
                "unsafe_scores": {
                    attr: result["attributeScores"][attr]["summaryScore"]["value"]
                    for attr in result["attributeScores"]
                },
            }
        )
    return results
