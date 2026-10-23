import os
import requests
from typing import List, Dict

def check_corpus_safety(texts: List[str]) -> Dict[str, Dict]:
    """
    Checks the safety of corpus text using Google Perspective API.
    Note: A valid PERSPECTIVE_API_KEY environment variable is required.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    results = {}

    for i, text in enumerate(texts):
        params = {
            "key": api_key
        }
        body = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "THREAT": {},
                "INSULT": {},
                "PROFANITY": {}
            },
            "languages": ["en"]
        }

        try:
            response = requests.post(endpoint, params=params, json=body)
            response.raise_for_status() # Raise an exception for HTTP errors
            analysis = response.json()
            
            text_results = {}
            for attr, data in analysis.get("attributeScores", {}).items():
                if "summaryScore" in data and "value" in data["summaryScore"]:
                    text_results[attr] = data["summaryScore"]["value"]
            results[f"Text {i+1}"] = text_results

        except requests.exceptions.RequestException as e:
            results[f"Text {i+1}"] = {"error": str(e)}
        
    return results

if __name__ == '__main__':
    sample_corpus = [
        "This is a perfectly normal sentence.",
        "You are an idiot!",
        "I will hurt you if you come near me.",
        "What a fantastic day it is."
    ]
    safety_scores = check_corpus_safety(sample_corpus)
    import json
    print(json.dumps(safety_scores, indent=2))
