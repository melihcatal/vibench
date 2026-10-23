import os
from typing import List
from googleapiclient import discovery
from googleapiclient.errors import HttpError


def check_corpus_safety(texts: List[str]) -> List[bool]:
    api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_CLOUD_API_KEY environment variable not set")

    client = discovery.build(
        "commentanalyzer", 
        "v1alpha1", 
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )
    service = client.comments()

    results = []
    for text in texts:
        try:
            analyze_request = {
                "comment": {"text": text},
                "requestedAttributes": {"TOXICITY": {}},
            }
            response = service.analyze(body=analyze_request).execute()
            toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            results.append(toxicity_score < 0.5)
        except HttpError as e:
            raise RuntimeError(f"Google Perspective API error: {e}")
    return results