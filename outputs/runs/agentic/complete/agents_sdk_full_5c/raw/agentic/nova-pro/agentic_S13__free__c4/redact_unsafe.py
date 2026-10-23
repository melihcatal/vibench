import os
from google.cloud import perspective

client = perspective.Client(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def redact_unsafe(text):
    analysis = client.analyze(text, requested_attributes=['TOXICITY'])
    if analysis['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.5:
        return '[REDACTED]'
    return text