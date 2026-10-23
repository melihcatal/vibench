import os
import deepl
from vision_models import VisualAnalysis, TranslatedText

def translate_text_deepl(text: str, target_language: str = "DE") -> TranslatedText:
    """
    Translates text using the DeepL API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "DE" for German).

    Returns:
        A TranslatedText object.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    
    # The deepl-python library uses DEEPL_SERVER_URL for enterprise vs free
    server_url = "https://api-free.deepl.com" if "fx" in auth_key.split(":")[-1].lower() else None

    translator = deepl.Translator(auth_key, server_url=server_url)
    
    result = translator.translate_text(text, target_lang=target_language)

    return TranslatedText(
        text=result.text,
        source_language=result.detected_source_lang,
        target_language=target_language,
        provider="deepl"
    )


def alt_text_translate(analysis: VisualAnalysis, target_language: str = "ES") -> VisualAnalysis:
    """

    Translates the image description (alt text) and adds it to the analysis object.
    
    Args:
        analysis: The VisualAnalysis object with a description.
        target_language: The language to translate the description into.
        
    Returns:
        The updated VisualAnalysis object.
    """
    if not analysis.description or not analysis.description.description:
        raise ValueError("Analysis object must have a description to translate.")
        
    translated_alt_text = translate_text_deepl(
        text=analysis.description.description,
        target_language=target_language
    )
    
    analysis.translated_description = translated_alt_text
    return analysis
