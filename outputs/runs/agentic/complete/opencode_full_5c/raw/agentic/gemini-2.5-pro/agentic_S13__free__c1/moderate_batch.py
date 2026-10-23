from typing import List, Dict
import time
from safety_client import get_perspective_client


def moderate_batch(texts: List[str]) -> List[Dict[str, float]]:
    """
    Analyzes a batch of texts for toxic content using the Perspective API.
    """
    client = get_perspective_client()
    results = []

    for text in texts:
        analyze_request = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
            },
        }

        response = client.comments().analyze(body=analyze_request).execute()

        scores = {}
        if "attributeScores" in response:
            for attribute, value in response["attributeScores"].items():
                scores[attribute] = value["summaryScore"]["value"]

        results.append(scores)
        # Adding a small delay to respect API rate limits for batch processing
        time.sleep(1)

    return results
