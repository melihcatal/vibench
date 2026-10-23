import os
from google.cloud import language_v1 as language
from stored_text_translate import translate_text
from typing import Optional, Dict

def summarize_asset(text: str, target_lang: str = 'en') -> Optional[Dict[str, str]]:
    """Generate a concise summary of a document using Google Cloud Natural Language.

    Args:
        text (str): Raw text extracted from the document.
        target_lang (str): Language to use for summarization (default 'en').

    Returns:
        Dict[str, str]: Dictionary with keys 'summary' and 'language'.
    """
    # If text is not in target language, translate first
    if target_lang != 'en' and text:
        translated = translate_text(text, target_lang=target_lang)
        if not translated:
            return None
        analysis_text = translated
    else:
        analysis_text = text or ''
    
    client = language.LanguageServiceClient()
    document = language.Document(content=analysis_text, type_=language.Document.Type.PLAIN_TEXT)
    response = client.annotate_text(request={'document': document, 'features': {'extract_summary': True}})
    summary = response.annotations.extracted_properties.summary or 'No summary available'
    return {'summary': summary[:500] if summary else '', 'language': response.language}
