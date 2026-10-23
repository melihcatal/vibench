import os
import json
from ibm_watsonx_ai.hap import harmful_content_detection as hcd
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')

authenticator = IAMAuthenticator(WATSONX_API_KEY)
detector = hcd.HarmfulContentDetectionV1(
    version='2024-08-08',
    service_url='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com',
    authenticator=authenticator,
)

def check_unsafe(payload: dict) -> bool:
    """Detect toxic/harmful language in message text using watsonx guardrails.","""
    text = payload.get('text', '')
    if not text:
        return False
    try:
        response = detector.detect_harmful_content(
            text=text,
            language='en',
        ).get_result()
        # Simple rule: if any toxic category score > 0.5, consider unsafe
        categories = response.get('categories', [])
        unsafe = any(cat.get('score', 0) > 0.5 for cat in categories)
        return unsafe
    except Exception as exc:
        print(f"Safety check error: {exc}")
        return False

if __name__ == '__main__':
    sample = {'text': 'Buy cheap viagra now!!!'}
    print('Unsafe?', check_unsafe(sample))
