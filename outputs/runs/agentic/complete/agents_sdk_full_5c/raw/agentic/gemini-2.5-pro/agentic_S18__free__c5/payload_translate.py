
import os
import deepl
from messaging_models import ProcessingResult

def translate_payload_text(text: str, target_lang: str, event_id: str) -> ProcessingResult:
    """
    Translates customer-facing message text using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR", "ES", "DE").
        event_id: The ID of the event being processed.

    Returns:
        A ProcessingResult object with the translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        # The provider is identified by the `deepl` SDK import and Translator class
        translator = deepl.Translator(auth_key)
        
        result = translator.translate_text(text, target_lang=target_lang)
        translated_text = result.text

        return ProcessingResult(
            original_event_id=event_id, 
            status="SUCCESS", 
            translation=translated_text
        )

    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return ProcessingResult(original_event_id=event_id, status="FAILURE", error_message=str(e))
    except Exception as e:
        print(f"An unexpected error occurred during translation: {e}")
        return ProcessingResult(original_event_id=event_id, status="FAILURE", error_message=str(e))

if __name__ == '__main__':
    # Example Usage:
    # Set the following environment variable before running:
    # export DEEPL_AUTH_KEY="your-deepl-auth-key"

    # text_to_translate = "Hello, world! This is a test of the translation service."
    # target_language = "FR"  # French
    # result = translate_payload_text(text_to_translate, target_language, "event-101")
    # print(result.to_dict())
    pass
