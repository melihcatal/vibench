import os
from googleapiclient import discovery
from vision_models import ImageLabel, TextSafetyScore
from typing import List

def check_label_safety(labels: List[ImageLabel]) -> List[TextSafetyScore]:
    """
    Checks generated visual labels for unsafe text using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Combine all label names into a single string to analyze.
    text_to_analyze = " ".join([label.name for label in labels])
    if not text_to_analyze.strip():
        return []

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text_to_analyze},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    
    scores = []
    for attribute, data in response['attributeScores'].items():
        score_value = data.get('summaryScore', {}).get('value', 0.0)
        scores.append(TextSafetyScore(attribute=attribute, score=score_value))
        
    return scores
