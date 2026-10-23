import os
from perspectiveapi.api import PerspectiveAPI

api = PerspectiveAPI(api_key=os.getenv('PERSPECTIVE_API_KEY'))

def check_safety(text):
    response = api.analyze(text)
    return response['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5