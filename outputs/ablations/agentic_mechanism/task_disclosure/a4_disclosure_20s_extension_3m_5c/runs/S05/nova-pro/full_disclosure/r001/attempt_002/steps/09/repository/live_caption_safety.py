import os
from perspective_api import PerspectiveAPI

def check_safety(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY environment variable not set')
    api = PerspectiveAPI(api_key)
    attributes = ['TOXICITY']
    result = api.analyze(text, attributes=attributes)
    toxicity_score = result['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score > 0.5

if __name__ == '__main__':\n    text = 'Sample unsafe text'
    is_unsafe = check_safety(text)
    print(f'Is the text unsafe? {is_unsafe}')
