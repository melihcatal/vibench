import os
import requests
from dotenv import load_dotenv

load_dotenv()


class LiveCaptionSafetyChecker:
    def __init__(self):
        self.PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
        if not self.PERSPECTIVE_API_KEY:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
        self.API_BASE_URL = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_safety(self, text):
        if not text:
            return {"score": 0.0, "summary": "No text to analyze."}

        url = f"{self.API_BASE_URL}?key={self.PERSPECTIVE_API_KEY}"
        payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            toxicity_score = (
                result.get("attributeScores", {})
                .get("TOXICITY", {})
                .get("summaryScore", {})
                .get("value", 0.0)
            )

            summary = (
                "Content is toxic." if toxicity_score > 0.5 else "Content is safe."
            )
            return {"score": toxicity_score, "summary": summary}
        except requests.exceptions.RequestException as e:
            return {"score": 0.0, "summary": f"Error checking safety: {e}"}
