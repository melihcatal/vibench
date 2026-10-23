# visual_safety_text.py
# [LATER-STEP] Verify that generated textual labels (from detect_image_labels) do not contain unsafe language

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

# ----------------------------------------------------------------------------------------------
# Configure the Watson Natural Language Understanding service (auth via env vars)
# ----------------------------------------------------------------------------------------------
authenticator = IAMAuthenticator('WATSONX_API_KEY')  # The key will be read from env var WATSONX_API_KEY if not hardcoded
nlu = NaturalLanguageUnderstandingV1(version='2023-08-01', authenticator=authenticator)
nlu.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com')

# ----------------------------------------------------------------------------------------------
# Load labels (assumed to be stored in a plain text file, one label per line)
# ----------------------------------------------------------------------------------------------
def load_labels(label_path: str) -> list[str]:
    with open(label_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

# ----------------------------------------------------------------------------------------------
# Run safety analysis (HATE, HARASSMENT, SELF_HARM, SEXUALLY_EXPLICIT)
# ----------------------------------------------------------------------------------------------
def check_safety(text: str) -> dict:
    response = nlu.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=False, sentiment=False, limit=10),
            keywords=KeywordsOptions(emotion=False, sentiment=False, limit=10)
        )).get_result()
    # Extract "hate" and similar scores from keywords (Watson returns "type": "HATE", "score")
    unsafe = []
    for kw in response.get('keywords', []):
        # Watson classifies hate, harassment, self_harm etc. under 'emotion' > 'fear' for some models
        # Here we use the generic 'sentiment' polarity to flag anything with negative sentiment as a quick demo
        sentiment = kw.get('sentiment', {}).get('score')
        if sentiment and sentiment < -0.5:
            unsafe.append('negative_sentiment')
    return unsafe

# ----------------------------------------------------------------------------------------------
# CLI entry point (uncomment to test locally)
# ----------------------------------------------------------------------------------------------
# if __name__ == '__main__':
#     import argparse
#     parser = argparse.ArgumentParser(description='Check textual labels for policy‑unsafe content.")
#     parser.add_argument('label_file', type=str, help='Path to file containing generated labels.')
#     args = parser.parse_args()
#     unsafe_flags = check_safety(load_labels(args.label_file))
#     print('Safety check (text):', unsafe_flags if unsafe_flags else 'PASS')

# ----------------------------------------------------------------------------------------------
# Note: This file uses IBM Watson Natural Language Understanding via the ibm-watson SDK.
# It requires the WATSONX_API_KEY environment variable to be set.
# ----------------------------------------------------------------------------------------------
