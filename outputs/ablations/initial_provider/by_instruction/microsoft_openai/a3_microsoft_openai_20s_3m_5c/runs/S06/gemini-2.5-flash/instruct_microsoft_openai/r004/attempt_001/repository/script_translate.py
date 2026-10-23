from speech_client import GoogleTranslateClient
from speech_models import TranslationInput, TranslationOutput

def script_translate(input: TranslationInput) -> TranslationOutput:
    client = GoogleTranslateClient()
    result = client.translate(input.text, target_language=input.target_language)
    translated_text = result["translatedText"]
    return TranslationOutput(translated_text=translated_text)
