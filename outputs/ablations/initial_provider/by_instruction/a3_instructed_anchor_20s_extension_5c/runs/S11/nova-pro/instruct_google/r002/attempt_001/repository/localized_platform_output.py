import os
from google.cloud import translate

def translate_text(project_id, text, target_language):
    client = translate.TranslationServiceClient()
    parent = f'projects/{project_id}/locations/global'
    response = client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    text = 'Hello, world!'
    target_language = 'es'
    result = translate_text(project_id, text, target_language)
    print(result)