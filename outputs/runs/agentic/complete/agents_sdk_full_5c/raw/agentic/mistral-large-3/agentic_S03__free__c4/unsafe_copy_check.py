from typing import List
import requests

class UnsafeCopyChecker:
    def __init__(self):
        self.api_key = "your-perspective-api-key"  # Placeholder for actual API key
        self.base_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def check_unsafe_content(self, texts: List[str]) -> List[dict]:
        results = []
        
        for text in texts:
            response = requests.post(
                self.base_url,
                params={"key": self.api_key},
                json={
                    "comment": {"text": text},
                    "languages": ["en"],  # Default to English for analysis
                    "requestedAttributes": {
                        "TOXICITY": {},
                        "SEVERE_TOXICITY": {},
                        "IDENTITY_ATTACK": {},
                        "INSULT": {},
                        "PROFANITY": {}
                    }
                }
            )
            
            if response.status_code == 200:
                results.append(response.json())
            else:
                results.append({"error": "Failed to analyze text"})
        
        return results