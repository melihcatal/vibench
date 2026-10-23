import os
from google.cloud import translate_v2 as translate

def translate_output(project_id, target_language, text):
    translate_client = translate.Client(project=project_id)
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    target_language = 'es'
    text = 'Hello, world!'
    translated_text = translate_output(project_id, target_language, text)
    print(translated_text)