import os
import deepl
from vision_models import ImageDescription, TranslatedText

def translate_description(
    description: ImageDescription, target_lang: str = "DE"
) -> TranslatedText:
    """
    Translates an image description using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(description.text, target_lang=target_lang)

    return TranslatedText(
        text=result.text,
        source_lang=result.detected_source_lang,
        target_lang=target_lang,
    )
