from google.cloud import translate_v2 as translate
from speech_models import FinalResult

translate_client = translate.Client()

def translate_caption(result: FinalResult, target_language: str = "es") -> str:
    text = result.transcript
    translation = translate_client.translate(text, target_language=target_language)
    return translation["translatedText"]