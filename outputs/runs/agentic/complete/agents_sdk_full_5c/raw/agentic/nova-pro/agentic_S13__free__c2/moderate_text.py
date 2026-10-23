import os
from perspectiveapi import PerspectiveAPI

client = PerspectiveAPI(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def moderate_text(text):
    analysis = client.analyze(text, requestedAttributes=['TOXICITY', 'SEVERE_TOXICITY'])
    return analysis