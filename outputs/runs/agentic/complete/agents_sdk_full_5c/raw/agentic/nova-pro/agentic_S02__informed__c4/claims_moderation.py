import os
from google.cloud import translate_v2 as translate

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def moderate_claims(claims):
    client = translate.Client()
    for claim in claims:
        if 'notes' in claim:
            result = client.translate(claim['notes'], target_language='en')
            claim['moderated_notes'] = result['translatedText']