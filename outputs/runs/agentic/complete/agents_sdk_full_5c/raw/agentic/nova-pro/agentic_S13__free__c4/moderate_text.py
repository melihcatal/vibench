import os
from google.cloud import perspective

client = perspective.Client(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def moderate_text(text):
    analysis = client.analyze(text, requested_attributes=['TOXICITY'])
    return analysis['attributeScores']['TOXICITY']['summaryScore']['value']