import os
from googleapiclient.discovery import build

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def moderate_profile(text):
    client = build('commentanalyzer', 'v1alpha1', developerKey=PERSPECTIVE_API_KEY)
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = client.comments().analyze(body=analyze_request).execute()
    return response['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5