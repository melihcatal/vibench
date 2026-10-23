import os
from google.cloud import translate

def translate_compliance_note(text, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path(os.getenv('GOOGLE_CLOUD_PROJECT'), 'us-central1')
    response = client.translate_text(parent=parent, contents=[text], target_language_code=target_language)
    return response.translations[0].translated_text

# Example usage (uncomment to test):
# translated_text = translate_compliance_note('your-text', 'es')