import os
import requests
from speech_client import get_transcribe_client

def moderate_transcript(transcript_text):
    # Use Perspective API as the concrete content moderation service
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    headers = {
        'Content-Type': 'application/json',
        'key': os.getenv('PERSPECTIVE_API_KEY')
    }
    payload = {
        'comment': {'text': transcript_text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    toxicity_score = result['attributeScores']['TOXICITY']['summaryScore']['value']
    print(f"Perspective toxicity score: {toxicity_score}")
    if toxicity_score > 0.8:
        moderated = "[REDACTED DUE TO HIGH TOXICITY]"
    else:
        moderated = transcript_text
    return moderated