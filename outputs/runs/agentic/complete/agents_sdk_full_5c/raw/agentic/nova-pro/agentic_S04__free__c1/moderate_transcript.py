from speech_client import get_comprehend_client

def moderate_transcript(text):
    comprehend = get_comprehend_client()
    response = comprehend.detect_toxic_content(Text=text, LanguageCode='en')
    return response