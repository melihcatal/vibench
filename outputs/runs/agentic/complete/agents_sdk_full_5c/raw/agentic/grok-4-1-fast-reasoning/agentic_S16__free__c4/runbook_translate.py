def translate_secret_runbook(notes: str, target_language: str = 'en') -> str:
    from google.cloud import translate_v2 as translate
    client = translate.Client()
    result = client.translate(notes, target_language=target_language)
    return result['translatedText']