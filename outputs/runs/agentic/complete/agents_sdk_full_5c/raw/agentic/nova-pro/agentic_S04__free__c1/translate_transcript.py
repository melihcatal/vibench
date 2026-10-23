from speech_client import get_translate_client

def translate_transcript(text, target_language='es'):
    translate = get_translate_client()
    response = translate.translate_text(Text=text, SourceLanguageCode='auto', TargetLanguageCode=target_language)
    return response