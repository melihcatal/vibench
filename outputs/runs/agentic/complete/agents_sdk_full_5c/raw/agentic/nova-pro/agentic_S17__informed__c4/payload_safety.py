from google.cloud import translate_v2 as translate

def check_payload_safety(text):
    translate_client = translate.Client()
    response = translate_client.translate(text, target_language='en')
    return response['translatedText']