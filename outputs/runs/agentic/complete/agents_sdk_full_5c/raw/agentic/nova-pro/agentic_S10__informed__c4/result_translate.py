from google.cloud import translate_v2 as translate

def translate_text(text, target_language='en'):
    translate_client = translate.Client.from_service_account_json('path/to/your-google-credentials.json')
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
