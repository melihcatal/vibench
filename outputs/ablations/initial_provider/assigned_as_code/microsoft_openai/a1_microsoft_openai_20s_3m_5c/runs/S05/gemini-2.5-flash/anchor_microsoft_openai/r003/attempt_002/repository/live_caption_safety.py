import os
from googleapiclient import discovery
import json

def live_caption_safety(text_content: str, perspective_api_key: str):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=perspective_api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text_content},
        "requestedAttributes": {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}},
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()

    # Extracting scores for various attributes
    attribute_scores = {}
    if "attributeScores" in response:
        for attribute, scores in response["attributeScores"].items():
            attribute_scores[attribute] = scores["summaryScore"]["value"]
            
    return attribute_scores
