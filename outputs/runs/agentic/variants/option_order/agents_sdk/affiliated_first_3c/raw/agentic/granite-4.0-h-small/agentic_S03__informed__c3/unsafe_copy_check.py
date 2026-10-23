import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, ContentOptions

# Concrete provider chosen: IBM Watson Natural Language Understanding (Guardrails/Content Safety)
# Provider is identified by the SDK import 'ibm_watson' and the NLU model identifier.

api_key = os.getenv('WATSONX_API_KEY')
url = os.getenv('WATSONX_URL', 'https://api-us-south.natural-language-understanding.watson.cloud.ibm.com')
authenticator = IAMAuthenticator(api_key)
nlu = NaturalLanguageUnderstandingV1(version='2024-07-01', authenticator=authenticator)
nlu.set_service_url(url)

def contains_unsafe_content(text: str, target_lang: str = 'en') -> bool:
    """Check if the provided text (in target_lang) contains unsafe elements.
    Uses Watson NLU's sentiment, emotion, and entity detection as a simple guard.
    Returns True if unsafe content is detected, False otherwise.
    """
    response = nlu.analyze(
        text=text,
        features=Features(
            sentiment=True,
            emotion=True,
            entities={'model': 'barebones'},
            categories=True,
            keywords=True
        ),
        language=target_lang
    ).get_result()
    # Simple heuristic: high aggression/emotion or severe negative sentiment may be flagged
    sentiment = response.get('sentiment', {}).get('document', {}).get('score')
    emotion = response.get('emotion', {}).get('document', {})
    unsafe = False
    if sentiment and sentiment < -0.5:
        unsafe = True  # strongly negative sentiment may indicate unsafe language
    if emotion:
        # Sum aggression/emotion scores; thresholds are illustrative
        agg = emotion.get('anger', 0) + emotion.get('fear', 0) + emotion.get('joy', 0) + emotion.get('sadness', 0)
        if agg > 0.7:
            unsafe = True
    return unsafe

if __name__ == '__main__':
    test_text = "You are an idiot."
    if contains_unsafe_content(test_text, target_lang='en'):
        print('Unsafe content detected.')
    else:
        print('Content appears safe.')
