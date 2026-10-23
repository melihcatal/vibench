import os
from google.cloud import perspective

def check_text_safety(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = perspective.Client(api_key)
    attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT']
    response = client.analyze(text, attributes)
    return response
