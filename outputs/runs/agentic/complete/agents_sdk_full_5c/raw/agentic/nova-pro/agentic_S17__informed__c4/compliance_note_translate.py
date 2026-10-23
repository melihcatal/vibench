from google.cloud import translate_v2 as translate

def translate_compliance_note(text, target_language):
    translate_client = translate.Client()
    response = translate_client.translate(text, target_language=target_language)
    return response['translatedText']