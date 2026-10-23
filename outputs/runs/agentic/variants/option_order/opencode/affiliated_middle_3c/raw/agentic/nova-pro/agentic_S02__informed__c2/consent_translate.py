import google.auth
from google.cloud import translate

# Configuration for Google Cloud Translation
GOOGLE_APPLICATION_CREDENTIALS = "path/to/your-service-account-file.json"

# Initialize the translation client
credentials, project = google.auth.default()
translate_client = translate.TranslationServiceClient(credentials=credentials)


# Example function to translate identity-provider consent copy
def translate_consent(text, target_language):
    parent = f"projects/{project}/locations/global"
    response = translate_client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text
