import os
from typing import List, Dict
from googleapiclient import discovery
from speech_models import ModerationRequest, ModerationResponse


def moderate_transcript(text: str) -> ModerationResponse:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()
    attribute_scores = response["attributeScores"]

    flagged_categories = []
    scores = {}
    for attribute, score_data in attribute_scores.items():
        score = score_data["summaryScore"]["value"]
        scores[attribute] = score
        if score > 0.7:
            flagged_categories.append(attribute)

    return ModerationResponse(
        is_flagged=len(flagged_categories) > 0,
        flagged_categories=flagged_categories,
        scores=scores,
    )
