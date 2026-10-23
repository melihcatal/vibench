import os
from google.cloud import perspective

client = perspective.Client(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def safety_threshold(text, threshold=0.5):
    analysis = client.analyze(text, requested_attributes=['TOXICITY'])
    toxicity_score = analysis['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score < threshold