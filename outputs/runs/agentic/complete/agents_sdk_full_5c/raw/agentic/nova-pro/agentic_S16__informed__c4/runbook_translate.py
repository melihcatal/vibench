from google.cloud import translate_v2 as translate

def runbook_translate(text, target_language):
    client = translate.Client()
    response = client.translate(text, target_language=target_language)
    return response['translatedText']