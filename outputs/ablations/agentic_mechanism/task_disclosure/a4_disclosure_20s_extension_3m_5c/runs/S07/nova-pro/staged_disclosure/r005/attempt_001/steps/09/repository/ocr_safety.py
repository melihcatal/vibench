import os
from google.cloud import perspective

def check_safety(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = perspective.Client(api_key)
    attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT']
    response = client.analyze(text, attributes)
    return response

if __name__ == '__main__':
    document_text = 'Sample document text to check for unsafe content.'
    result = check_safety(document_text)
    print(result)