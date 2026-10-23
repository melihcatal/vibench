import os
import json
from ibm_watsonx_ai.nlp import natural_language_understanding as nlu
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Watsonx.ai configuration (using Granite model for summarization)
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
GRAMMAR_MODEL_ID = os.getenv('SUMMARIZATION_MODEL_ID', 'granite-13b-natural-language-understanding')

authenticator = IAMAuthenticator(WATSONX_API_KEY)
nlu_client = nlu.NaturalLanguageUnderstandingV1(
    version='2024-08-08',
    service_url='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com',
    authenticator=authenticator,
)

def summarize(event_payload: dict) -> str:
    """
    Summarizes the message text using Granite via watsonx.ai.
    Expects the payload to contain a field 'text'.
    Returns a short summary string.
    """
    text = event_payload.get('text', '')
    if not text:
        return "<no text provided>"
    try:
        response = nlu_client.summarize(
            text=text,
            language='en',
            model_id=GRAMMAR_MODEL_ID,
        ).get_result()
        summary = response.get('summary', '')
        return summary[:500]  # truncate for safety
    except Exception as exc:
        print(f"Summarization error: {exc}")
        return "Summarization failed"

if __name__ == '__main__':
    sample = {'text': 'The quick brown fox jumps over the lazy dog. It was a bright cold day in April, and the clocks were striking thirteen.'}
    print('Sample summary:', summarize(sample))
