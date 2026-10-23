import os
from perspectiveapi.client import PerspectiveAPI

# Initialize the Perspective API client
perspective_api = PerspectiveAPI(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def check_safety(text):
    """Check if the given text contains unsafe content."""
    attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT']
    response = perspective_api.analyze(text, attributes=attributes)
    for attribute in attributes:
        if response['attributeScores'][attribute]['summaryScore']['value'] > 0.5:
            return False
    return True