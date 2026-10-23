import os
from perspective_api import PerspectiveAPI

def moderate_batch(messages):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY environment variable not set')
    client = PerspectiveAPI(api_key)
    results = []
    for message in messages:
        analysis = client.analyze(message, ['TOXICITY'])
        toxicity_score = analysis['attributeScores']['TOXICITY']['summaryScore']['value']
        results.append({'message': message, 'toxicity_score': toxicity_score})
    return results

if __name__ == '__main__':
    messages = ['Hello, world!', 'This is a toxic message.']
    print(moderate_batch(messages))