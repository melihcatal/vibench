import os
from perspectiveapi.client import PerspectiveClient

def check_log_text_safety(log_text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = PerspectiveClient(api_key)
    attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT']
    response = client.analyze(log_text, attributes=attributes)
    return response

if __name__ == '__main__':
    log_text = 'Example log message text'
    safety_check_result = check_log_text_safety(log_text)
    print(safety_check_result)