import os
from google.cloud import perspective

def check_unsafe_content(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = perspective.Client(api_key=api_key)
    attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT']
    response = client.analyze(text, attributes=attributes)
    return response

if __name__ == '__main__':
    transcript_text = 'Enter live transcript text here'
    result = check_unsafe_content(transcript_text)
    print(result)