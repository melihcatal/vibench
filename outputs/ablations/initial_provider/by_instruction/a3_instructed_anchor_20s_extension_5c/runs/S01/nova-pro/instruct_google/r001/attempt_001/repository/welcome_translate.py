from google.cloud import translate

# Configuration
PROJECT_ID = 'your-project-id'

# Initialize client
client = translate.TranslationServiceClient()

# Function to translate onboarding copy
def translate_onboarding_copy(text, target_language_code):
    parent = f'projects/{PROJECT_ID}/locations/global'
    response = client.translate_text(parent=parent, contents=[text], target_language_code=target_language_code)
    return response.translations[0].translated_text