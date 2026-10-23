from google.cloud import translate



def translate_transcript(transcript, target_language):
    client = translate.TranslateClient()
    translation = client.translate(transcript, target_language=target_language)
    return translation["translatedText"]