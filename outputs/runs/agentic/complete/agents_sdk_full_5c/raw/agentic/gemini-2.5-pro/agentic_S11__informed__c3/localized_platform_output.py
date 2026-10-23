import os
import deepl
from model_models import TranslationRequest, TranslationResponse

def translate_text_deepl(request: TranslationRequest) -> TranslationResponse:
    """
    Translates text using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            request.text,
            target_lang=request.target_language
        )
        return TranslationResponse(
            translated_text=result.text,
            detected_source_language=result.detected_source_lang
        )
    except deepl.DeepLException as e:
        print(f"Error during DeepL translation: {e}")
        raise

if __name__ == '__main__':
    # This part is for demonstration if run directly
    req = TranslationRequest(
        text="Hello, world!",
        target_language="FR" # French
    )
    response = translate_text_deepl(req)
    print(f"Original: {req.text}")
    print(f"Translated ({response.detected_source_language} -> {req.target_language}): {response.translated_text}")
