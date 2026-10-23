import os
from perspectiveapi import PerspectiveApiClient

# Initialize the client with your API key
api_key = os.getenv('PERSPECTIVE_API_KEY')
client = PerspectiveApiClient(api_key=api_key)

def moderate_batch(messages):
    results = []
    for message in messages:
        response = client.analyze_comment(
            comment=message,
            requestedAttributes=['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT']
        )
        results.append({
            'message': message,
            'decision': 'unsafe' if response.attributeScores['TOXICITY'].summaryScore.value > 0.5 else 'safe'
        })
    return results