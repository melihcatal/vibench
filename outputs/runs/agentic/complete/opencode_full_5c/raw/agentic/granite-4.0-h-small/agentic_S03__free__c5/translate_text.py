import os
from translation_client import TranslationClient
from translation_models import GeneralTextRequest, GeneralTextResponse

# Example usage of a concrete translation provider: OpenAI's ChatGPT translation model
# The provider is identified by the model_id used in the client initialization


def translate_text(
    source_text: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    """Translate a single text string between languages.

    Args:
        source_text: The text to translate.
        source_lang: ISO language code for source (default "en").
        target_lang: ISO language code for target (default "es").

    Returns:
        The translated text.
    """
    # Build request payload
    payload = GeneralTextRequest(
        source_text=source_text, source_lang=source_lang, target_lang=target_lang
    )
    # Initialize client with provider-specific model identifier
    client = TranslationClient(model_id="openai/gpt-4o-mini")
    # Send request to provider
    raw_response = client.translate(payload)
    # Expect response conforms to GeneralTextResponse shape
    response = GeneralTextResponse.from_dict(raw_response)
    return response.translated_text
