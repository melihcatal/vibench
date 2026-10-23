import os
import requests
from typing import List, Dict


def check_corpus_safety(texts: List[str]) -> List[Dict]:
    """
    Checks the safety of corpus text before embedding using the Perspective API.
    """
    perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"
    results = []

    for text in texts:
        request_body = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {},
                "FLIRTATION": {},
                "INSULT": {},
            },
            "languages": ["en"],  # Specify language if known, or let API detect
        }
        try:
            response = requests.post(api_url, json=request_body)
            response.raise_for_status()  # Raise an exception for HTTP errors
            analysis_result = response.json()
            results.append({"text": text, "analysis": analysis_result})
        except requests.exceptions.RequestException as e:
            results.append({"text": text, "error": str(e)})

    return results


if __name__ == "__main__":
    sample_corpus_texts = [
        "This is a perfectly normal and safe sentence.",
        "I hate you, you are so stupid!",
        "Let's discuss the project details peacefully.",
        "You are an idiot and should be banned.",
    ]

    safety_checks = check_corpus_safety(sample_corpus_texts)
    for result in safety_checks:
        print(f"Text: '{result['text']}'")
        if "error" in result:
            print(f"  Error: {result['error']}")
        else:
            for attribute, scores in (
                result["analysis"].get("attributeScores", {}).items()
            ):
                summary_score = scores.get("summaryScore", {}).get("value")
                print(f"  {attribute}: {summary_score}")
        print("-" * 20)
