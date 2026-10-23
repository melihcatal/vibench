import os
from googleapiclient import discovery

API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_live_caption_safety(text: str):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    is_unsafe = toxicity_score > 0.7

    return {"is_unsafe": is_unsafe, "toxicity_score": toxicity_score}
