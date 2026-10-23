import os
from perspective_api import PerspectiveAPI

def check_unsafe_content(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    api = PerspectiveAPI(api_key)
    analysis = api.analyze(text, ['TOXICITY'])
    return analysis['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.5

if __name__ == '__main__'):
    localized_copy = 'Example localized copy text'
    is_unsafe = check_unsafe_content(localized_copy)
    print(f'Is unsafe: {is_unsafe}')
