import speech_client
import google.cloud.translate

def live_caption_translate(transcript, target_language):
    translate_client = google.cloud.translate.Client()
    translation = translate_client.translate(transcript, target_language=target_language)
    return translation['translatedText']