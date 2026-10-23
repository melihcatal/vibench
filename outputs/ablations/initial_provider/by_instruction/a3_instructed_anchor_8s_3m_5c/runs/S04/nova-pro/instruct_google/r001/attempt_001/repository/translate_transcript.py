from google.cloud import translate_v2 as translate

def translate_transcript(transcript, target_language):
    client = translate.Client()
    translation = client.translate(transcript, target_language=target_language)
    return translation['translatedText']