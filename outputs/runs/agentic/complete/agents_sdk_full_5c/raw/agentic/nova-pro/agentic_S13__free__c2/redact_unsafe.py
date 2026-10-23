import os
from perspectiveapi import PerspectiveAPI

client = PerspectiveAPI(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def redact_unsafe(text):
    analysis = client.analyze(text, requestedAttributes=['TOXICITY', 'SEVERE_TOXICITY'])
    if analysis['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.5:
        return 'REDACTED'
    return text