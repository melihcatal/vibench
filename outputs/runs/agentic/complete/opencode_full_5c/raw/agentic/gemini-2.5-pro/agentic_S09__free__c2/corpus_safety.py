import os
from googleapiclient import discovery


def check_corpus_safety(text: str):
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    scores = {
        attr: response["attributeScores"][attr]["summaryScore"]["value"]
        for attr in response["attributeScores"]
    }
    return scores
