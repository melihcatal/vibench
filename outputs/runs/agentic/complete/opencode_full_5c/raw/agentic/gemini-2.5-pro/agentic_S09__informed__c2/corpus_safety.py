import os
import requests
from typing import List, Dict


def check_corpus_safety(corpus: List[str]) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    results = {}
    for text in corpus:
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            toxicity_score = data["attributeScores"]["TOXICITY"]["summaryScore"][
                "value"
            ]
            results[text] = toxicity_score
        except requests.exceptions.RequestException as e:
            results[text] = -1.0  # Indicate error
            print(f"Error checking safety for text: '{text}'. Error: {e}")

    return results
