"""
Translate HTML or markup while preserving tags using Google Cloud Translation API v3.
"""
from translation_client import create_default_client
from translation_models import MarkupTranslationRequest, split_html_content, reassemble_html


def translate_markup(
    html_content: str,
    target_language: str,
    source_language: str = None,
    preserve_formatting: bool = True,
    model: str = None,
) -> str:
    """
    Translate HTML or markup content while preserving tags and structure.
    
    Uses Google Cloud Translation v3 API (translate.googleapis.com) with mime_type
    set to 'text/html' which instructs the Google NMT model to preserve HTML tags
    and only translate the text content between tags.
    
    Args:
        html_content: HTML string to translate
        target_language: Target language code
        source_language: Source language code (optional)
        preserve_formatting: Whether to preserve HTML formatting (default True)
        model: Specific Google model to use (e.g., nmt or base)
    
    Returns:
        Translated HTML string with original tags preserved
    """
    client = create_default_client()
    
    mime_type = "text/html" if preserve_formatting else "text/plain"
    
    if preserve_formatting:
        parsed = split_html_content(html_content)
        
        if parsed["translatable_texts"]:
            trans_response = client.batch_translate(
                texts=parsed["translatable_texts"],
                target_language=target_language,
                source_language=source_language,
                mime_type=mime_type,
                model=model,
            )
            
            translated_texts = [
                t.translated_text for t in trans_response.translations
            ]
            
            return reassemble_html(parsed["segments"], translated_texts)
        else:
            return html_content
    
    response = client.translate_html(
        html_content=html_content,
        target_language=target_language,
        source_language=source_language,
        model=model,
    )
    
    return response.translated_text


if __name__ == "__main__":
    html_example = """
    <html>
        <body>
            <h1>Welcome</h1>
            <p>This is a <strong>sample</strong> paragraph with <em>emphasis</em>.</p>
            <a href="https://example.com">Click here</a>
        </body>
    </html>
    """
    
    result = translate_markup(
        html_content=html_example,
        target_language="fr",
        source_language="en",
    )
    print(result)
