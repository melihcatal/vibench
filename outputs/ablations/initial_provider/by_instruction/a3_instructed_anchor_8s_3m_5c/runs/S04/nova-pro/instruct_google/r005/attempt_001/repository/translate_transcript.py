from google.cloud import translate_v2 as translate

def translate_transcript(transcript: str, target_language: str):
    client = translate.Client()
    translation = client.translate(transcript, target_language=target_language)
    return translation['translatedText']