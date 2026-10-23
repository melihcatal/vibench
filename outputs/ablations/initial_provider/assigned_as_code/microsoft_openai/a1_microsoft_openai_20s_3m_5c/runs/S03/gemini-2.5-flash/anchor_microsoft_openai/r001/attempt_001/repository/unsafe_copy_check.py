from googleapiclient import discovery
import json
import os

def check_unsafe_content(payload, config=None):
    config = config or {}
    
    # Initialize the Perspective API client
    # Ensure GOOGLE_API_KEY environment variable is set for API key authentication
    # Or pass it in config as 'api_key'
    api_key = config.get('api_key') or os.environ.get('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError("Perspective API key must be provided or set as PERSPECTIVE_API_KEY environment variable.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    text_to_analyze = payload['localized_text']

    analyze_request = {
        'comment': { 'text': text_to_analyze },
        'requestedAttributes': { 'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {} }
    }

    response = client.comments().analyze(body=analyze_request).execute()

    attribute_scores = {}
    for attribute, data in response['attributeScores'].items():
        attribute_scores[attribute] = data['summaryScore']['value']

    # Determine if any attribute score indicates unsafe content (e.g., score > 0.5)
    is_unsafe = any(score > 0.5 for score in attribute_scores.values())

    return {
        'localized_text': text_to_analyze,
        'attribute_scores': attribute_scores,
        'is_unsafe': is_unsafe,
        'notes': "Scores range from 0 to 1, where higher values indicate a greater perceived likelihood of the attribute being true for the text."
    }
