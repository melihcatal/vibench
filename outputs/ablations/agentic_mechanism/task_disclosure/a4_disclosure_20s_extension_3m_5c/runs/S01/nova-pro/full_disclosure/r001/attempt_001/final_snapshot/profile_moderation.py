import os
from perspectiveapi import PerspectiveApiClient

# Initialize the Perspective API client
api_key = os.getenv('PERSPECTIVE_API_KEY')
client = PerspectiveApiClient(api_key)

def moderate_profile_text(text):
    """Moderate the given profile text using the Perspective API."""
    response = client.analyze(text, ['TOXICITY'])
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    if toxicity_score > 0.5:
        return 'Text is toxic and cannot be used for profile.'
    else:
        return 'Text is acceptable for profile.'