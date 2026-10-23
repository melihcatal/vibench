import os
import requests

# Set environment variables
os.environ['PERSPECTIVE_API_KEY'] = 'your-perspective-api-key'

# Check message payload text for unsafe content
message = 'Message payload text...'
response = requests.post(
    'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze',
    json={
        'comment': {'text': message},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}},
    },
    params={'key': os.getenv('PERSPECTIVE_API_KEY')}
)
print(response.json()