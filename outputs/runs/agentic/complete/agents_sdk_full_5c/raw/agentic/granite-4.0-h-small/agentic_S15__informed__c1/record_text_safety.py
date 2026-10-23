import os
import requests
from typing import Dict

# Managed Text Safety service: AWS Comprehend (DetectPii/Profanity) via Comprehend API
# For demo we use the Comprehend endpoint directly; in production guard with API key/role.
BASE_URL = 'https://comprehend.us-east-1.amazonaws.com'
# Assuming IAM role attached to Lambda/EC2 provides required permissions.

API_KEY = os.getenv('AWS_ACCESS_KEY_ID')  # placeholder; real usage via boto3 client is recommended

def check_text_safety(text: str) -> Dict[str, bool]:
    """Run AWS Comprehend toxicity/profanity detection on supplied text.

    Returns dict with keys:
        'toxic': True if toxic,
        'profanity': True if contains profanity,
        'pii_entities': list of found PII entity dicts.
    """
    payload = {
        'Text': text,
        'LanguageCode': 'en'
    }
    response = requests.post(
        f'{BASE_URL}/DetectPiiEntities',
        json=payload,
        timeout=10
    )
    if response.status_code != 200:
        raise RuntimeError(f'Comprehend error: {response.status_code} {response.text}')
    data = response.json()
    return {
        'toxic': data.get('Toxicity', 0) > 0.5,
        'profanity': data.get('ProfanityScore', 0) > 0.5,
        'pii_entities': data.get('PiiEntities', [])
    }

if __name__ == "__main__":
    # Demo run
    result = check_text_safety('This is a test with some profanity ---- asshole!')
    print('Safety result:', result)
