import os
from googleapiclient.discovery import build

# Set up the API client
API_KEY = os.getenv('PERSPECTIVE_API_KEY')
API_NAME = 'commentanalyzer'
API_VERSION = 'v1alpha1'
service = build(API_NAME, API_VERSION, developerKey=API_KEY)

def check_unsafe_content(text):
    """Check if the given text contains unsafe content."""
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = service.comments().analyze(body=analyze_request).execute()
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
    return toxicity_score > 0.5

if __name__ == '__main__':
    transcript_text = 'Sample live transcript text to check for unsafe content.'
    is_unsafe = check_unsafe_content(transcript_text)
    print(f'Is the transcript text unsafe? {is_unsafe}')
