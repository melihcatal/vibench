from googleapiclient import discovery
import json

def check_annotation_safety(payload, api_key):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': payload["text"]},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()

    # Extract attribute scores
    attribute_scores = {}
    for attribute, data in response.get("attributeScores", {}).items():
        attribute_scores[attribute] = data["summaryScore"]["value"]

    # Determine if considered unsafe (e.g., any score above a threshold)
    is_unsafe = any(score > payload.get("threshold", 0.7) for score in attribute_scores.values())

    return {
        "text": payload["text"],
        "is_unsafe": is_unsafe,
        "scores": attribute_scores
    }
