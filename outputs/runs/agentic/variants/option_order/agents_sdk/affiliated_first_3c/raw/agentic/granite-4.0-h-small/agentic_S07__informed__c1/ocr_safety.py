import boto3
import json

# Content safety check using Amazon Comprehend (toxicity detection example)
comprehend_client = boto3.client('comprehend')

def check_text_safety(text: str) -> List[str]:
    '''Check extracted document text for unsafe content using Amazon Comprehend.
    Returns a list of detected issues such as 'TOXICITY'.
    '''
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    # Basic example: Comprehend does not have a dedicated toxicity API.
    # You could replace this with Bedrock Guardrails or Perspective API as needed.
    # Here we simply note sentiment, and call out the limitation.
    sentiment = response['Sentiment']
    issues = []
    if sentiment == 'NEGATIVE':
        issues.append('NEGATIVE_SENTIMENT')
    return issues

# Alternative implementation placeholder:
# def check_safety_perspective(text: str):
#     headers = {'Authorization': f'Bearer {os.getenv("PERSPECTIVE_API_KEY")}'}
#     payload = {'comment': {'text': text, 'type': 'PLAIN_TEXT'} , 'context': ...}
#     response = requests.post('https://commentanalyzer.googleapis.com/v1beta1/comments:analyze', headers=headers, json=payload).json()
#     return [issue['type'] for issue in response.get('attributeScores', {}).values() if issue['summaryScore']['value'] > 0.8]
