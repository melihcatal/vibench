import os
import requests
import json
from typing import List, Dict, Any


def check_text_safety(corpus: List[str]) -> List[Dict[str, Any]]:
    """
    Checks corpus text for toxicity using the Perspective API before embedding.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    results = []

    for text in corpus:
        request_body = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}},
        }

        try:
            response = requests.post(url, data=json.dumps(request_body))
            response.raise_for_status()
            response_data = response.json()

            toxicity_score = response_data["attributeScores"]["TOXICITY"][
                "summaryScore"
            ]["value"]
            is_safe = toxicity_score < 0.7

            results.append(
                {"text": text, "toxicity_score": toxicity_score, "is_safe": is_safe}
            )
        except requests.exceptions.RequestException as e:
            results.append({"text": text, "error": str(e), "is_safe": False})

    return results


if __name__ == "__main__":
    # This is an example and will not be executed
    sample_corpus = [
        "This is a perfectly fine and respectable comment.",
        "You are a wonderful person and a great contributor.",
        "I hate you and everything you stand for.",
    ]
    safety_results = check_text_safety(sample_corpus)
    for result in safety_results:
        print(result)
