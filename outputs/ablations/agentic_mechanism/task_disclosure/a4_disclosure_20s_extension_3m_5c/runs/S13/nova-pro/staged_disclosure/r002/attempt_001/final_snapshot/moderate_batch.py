import os
from perspectiveapi import PerspectiveAPI

def moderate_batch(messages):
    api = PerspectiveAPI(api_key=os.getenv('PERSPECTIVE_API_KEY'))
    results = []
    for message in messages:
        analysis = api.analyze(message, ['TOXICITY'])
        results.append({'message': message, 'toxicity': analysis['TOXICITY']['score']})
    return results

if __name__ == '__main__':
    messages = ['Hello, how are you?', 'This is a toxic message.']
    print(moderate_batch(messages))