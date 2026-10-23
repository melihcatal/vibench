"""
Translates HTML or markup while preserving tags.
Uses Google Cloud Translation API (google.cloud.translate_v2) with format='html'
for markup-aware translation.
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google Neural Machine Translation (NMT) with HTML format support
"""

from typing import Optional

from translation_client import create_translate_client
from translation_models import (
    MarkupTranslationRequest,
    TranslationResponse,
    TranslationResult,
    normalize_language_code,
    split_markup_into_segments,
    reassemble_markup,
)


def translate_markup(
    markup_text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
    tag_pattern: str = r"<[^>]+>",
) -> TranslationResponse:
    """
    Translate HTML or markup text while preserving all tags and structure.
    
    Uses the google.cloud.translate_v2 client with format_='html' to perform
    markup-aware translation via the translate.googleapis.com endpoint.
    HTML tags are preserved and only translatable text content is translated.
    
    Args:
        markup_text: HTML or markup text to translate.
        target_language: Target language code (ISO 639-1).
        source_language: Source language code (ISO 639-1). Auto-detected if None.
        project_id: Google Cloud project ID.
        credentials_path: Path to service account credentials JSON.
        tag_pattern: Regex pattern for matching markup tags.
    
    Returns:
        TranslationResponse with translated markup preserving all tags.
    """
    client = create_translate_client(
        project_id=project_id,
        credentials_path=credentials_path,
    )
    
    target_lang = normalize_language_code(target_language)
    source_lang = normalize_language_code(source_language) if source_language else None
    
    request = MarkupTranslationRequest(
        markup_text=markup_text,
        source_language=source_lang,
        target_language=target_lang,
        tag_pattern=tag_pattern,
    )
    
    segments = split_markup_into_segments(markup_text, tag_pattern=tag_pattern)
    text_segments = [seg for seg in segments if seg["type"] == "text"]
    
    if not text_segments:
        return TranslationResponse(
            results=[TranslationResult(
                translated_text=markup_text,
                source_language="unknown",
                target_language=target_lang,
                original_text=markup_text,
                confidence=1.0,
                model_used="google-translate-v2-nmt",
            )],
            success=True,
        )
    
    text_contents = [seg["content"] for seg in text_segments]
    
    translate_kwargs = {
        "values": text_contents,
        "target_language": target_lang,
        "format_": "html",
    }
    
    if source_lang:
        translate_kwargs["source_language"] = source_lang
    
    try:
        results = client.translate(**translate_kwargs)
        
        translated_texts = []
        if isinstance(results, list):
            for result in results:
                translated = result.get("translatedText", "") if isinstance(result, dict) else result
                translated_texts.append(translated)
        
        translated_idx = 0
        for seg in segments:
            if seg["type"] == "text" and translated_idx < len(translated_texts):
                seg["content"] = translated_texts[translated_idx]
                translated_idx += 1
        
        translated_markup = reassemble_markup(segments)
        
        detected_source = "unknown"
        if isinstance(results, list) and len(results) > 0:
            first_result = results[0]
            if isinstance(first_result, dict):
                detected_source = first_result.get("detectedSourceLanguage", "unknown")
        
        return TranslationResponse(
            results=[TranslationResult(
                translated_text=translated_markup,
                source_language=detected_source,
                target_language=target_lang,
                original_text=markup_text,
                confidence=1.0,
                model_used="google-translate-v2-nmt-html",
            )],
            success=True,
        )
    
    except Exception as e:
        return TranslationResponse(
            results=[],
            success=False,
            error_message=f"Google Markup Translation API error: {str(e)}",
        )


if __name__ == "__main__":
    html = "<p>Hello <strong>world</strong>!</p><a href='#'>Click here</a>"
    response = translate_markup(html, target_language="de")
    if response.success:
        print(response.results[0].translated_text)
