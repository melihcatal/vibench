import os
from perspectiveapi import PerspectiveAPI

client = PerspectiveAPI(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def safety_threshold(text, threshold=0.5):
    analysis = client.analyze(text, requestedAttributes=['TOXICITY'])
    if analysis['attributeScores']['TOXICITY']['summaryScore']['value'] < threshold:
        return True
    return False