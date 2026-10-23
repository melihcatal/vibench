import os
from perspectiveapi import PerspectiveAPI

def check_unsafe_copy(text):
    os.environ['PERSPECTIVE_API_KEY'] = 'your-perspective-api-key'
    api = PerspectiveAPI()
    result = api.analyze(text, ['TOXICITY'])
    return result['attributeScores']['TOXICITY']['summaryScore']['value'] < 0.5