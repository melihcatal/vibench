from google.cloud import translate_v2 as translate

def translate_consent(text, target_language):
    translate_client = translate.Client.from_service_account_json('path/to/your-service-account-file.json')
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']