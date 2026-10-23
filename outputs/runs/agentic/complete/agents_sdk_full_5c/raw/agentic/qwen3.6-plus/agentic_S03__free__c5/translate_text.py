"""
Translate a single text string between languages using Google Cloud Translation API v3.
"""
from translation_client import create_default_client
from translation_models import TranslationRequest


def translate_text(
    text: str,
    target_language: str,
    source_language: str = None,
    format: str = "text",
    glossary: dict = None,
    model: str = None,
) -> str:
    """
    Translate a single text string between languages using Google Cloud Translation.
    
    Uses the Google Cloud Translation v3 API with the NMT (Neural Machine Translation)
    model hosted at translate.googleapis.com.
    """
    request = TranslationRequest(
        source_text=text,
        source_language=source_language,
        target_language=target_language,
        format=format,
        glossary=glossary,
        model=model,
    )

    client = create_default_client()

    mime_type = "text/html" if request.format == "html" else "text/plain"

    response = client.translate_text(
        text=request.source_text,
        target_language=request.target_language,
        source_language=request.source_language,
        mime_type=mime_type,
        model=request.model,
    )

    return response.translated_text


if __name__ == "__main__":
    result = translate_text(
        text="Hello, welcome to our application.",
        target_language="es",
        source_language="en",
    )
    print(f"Translation: {result}")
