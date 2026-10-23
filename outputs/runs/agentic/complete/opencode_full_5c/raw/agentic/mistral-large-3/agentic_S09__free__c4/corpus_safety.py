from typing import List
import requests
import os


def corpus_safety(texts: List[str]) -> Dict[str, List[str]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    unsafe_texts = []

    for text in texts:
        params = {"key": api_key}
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
            },
            "languages": ["en"],
        }

        response = requests.post(url, params=params, json=payload)
        if response.status_code != 200:
            raise ValueError(f"Perspective API request failed: {response.text}")

        result = response.json()
        toxicity_score = (
            result.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0)
        )

        if toxicity_score > 0.7:
            unsafe_texts.append(text)

    return {"safe": [t for t in texts if t not in unsafe_texts], "unsafe": unsafe_texts}
