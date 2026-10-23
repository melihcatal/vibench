import os
from perspectiveapi import PerspectiveAPI

def moderate_profile_text(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    papi = PerspectiveAPI(api_key)
    analysis = papi.analyze(text, ['TOXICITY', 'IDENTITY_ATTACK'])
    return analysis