import os
import requests
import json

class SafetyCheckResult:
    def __init__(self, overall_score: float, attributes: dict):
        self.overall_score = overall_score
        self.attributes = attributes

def check_content_safety(text: str) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Example attributes to request, adjust as needed
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': requested_attributes
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status() # Raise an exception for bad status codes

    result = response.json()

    overall_score = 0.0
    attribute_scores = {}

    if 'attributeScores' in result:
        for attr, scores in result['attributeScores'].items():
            summary_score = scores['summaryScore']['value']
            attribute_scores[attr] = summary_score
            if attr == 'TOXICITY': # Use TOXICITY as a primary indicator for overall score
                overall_score = summary_score

    return SafetyCheckResult(overall_score=overall_score, attributes=attribute_scores)
