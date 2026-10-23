from google.cloud import translate


def translate_transcript(text, target_language):
    client = translate.TranslateClient()
    translation = client.translate(text, target_language=target_language)
    return translation["translatedText"]