import os
from google.cloud import perspective

client = perspective.Client(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def moderate_batch(texts):
    results = []
    for text in texts:
        analysis = client.analyze(text, requested_attributes=['TOXICITY'])
        results.append(analysis['attributeScores']['TOXICITY']['summaryScore']['value'])
    return results