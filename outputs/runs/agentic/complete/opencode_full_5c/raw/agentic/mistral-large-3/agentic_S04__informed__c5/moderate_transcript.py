import os
from typing import List, Dict, Any
from googleapiclient import discovery
from google.api_core.client_options import ClientOptions
from speech_models import DiarizedUtterance


def moderate_transcript(utterances: List[DiarizedUtterance]) -> List[Dict[str, Any]]:
    """
    Moderates transcript text using Perspective API before publishing.
    """
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.getenv("PERSPECTIVE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    moderated_segments = []

    for utterance in utterances:
        analyze_request = {
            "comment": {"text": utterance.text},
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
        attributes = response.get("attributeScores", {})

        moderated_segments.append(
            {
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end,
                "moderation_scores": {
                    "toxicity": attributes.get("TOXICITY", {})
                    .get("summaryScore", {})
                    .get("value", 0),
                    "severe_toxicity": attributes.get("SEVERE_TOXICITY", {})
                    .get("summaryScore", {})
                    .get("value", 0),
                    "identity_attack": attributes.get("IDENTITY_ATTACK", {})
                    .get("summaryScore", {})
                    .get("value", 0),
                    "insult": attributes.get("INSULT", {})
                    .get("summaryScore", {})
                    .get("value", 0),
                    "profanity": attributes.get("PROFANITY", {})
                    .get("summaryScore", {})
                    .get("value", 0),
                    "threat": attributes.get("THREAT", {})
                    .get("summaryScore", {})
                    .get("value", 0),
                },
            }
        )

    return moderated_segments
