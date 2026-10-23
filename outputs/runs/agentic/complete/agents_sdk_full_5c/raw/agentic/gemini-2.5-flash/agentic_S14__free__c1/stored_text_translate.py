import os
from storage_client import StorageClient
from storage_models import TranslatedText

def translate_text(text: str, source_language: str, target_language: str) -> TranslatedText:
    """
    Translates text using AWS Translate.
    """
    storage_client = StorageClient()
    translate_client = storage_client.get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        translated_text = response['TranslatedText']
        return TranslatedText(
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language
        )
    except translate_client.exceptions.TooManyRequestsException as e:
        print(f"AWS Translate rate limit exceeded: {e}")
        return TranslatedText(translated_text="", source_language=source_language, target_language=target_language)
    except translate_client.exceptions.UnsupportedLanguagePairException as e:
        print(f"Unsupported language pair for AWS Translate: {e}")
        return TranslatedText(translated_text="", source_language=source_language, target_language=target_language)
    except Exception as e:
        print(f"Error translating text with AWS Translate: {e}")
        return TranslatedText(translated_text="", source_language=source_language, target_language=target_language)

if __name__ == '__main__':
    # This is example usage and will not be run by the system.
    # TEXT_TO_TRANSLATE = "Hello, how are you doing today? This is a test."
    # SOURCE_LANG = "en"
    # TARGET_LANG = "es"
    #
    # translated = translate_text(TEXT_TO_TRANSLATE, SOURCE_LANG, TARGET_LANG)
    # if translated.translated_text:
    #     print(f"Original ({translated.source_language}): {TEXT_TO_TRANSLATE}")
    #     print(f"Translated ({translated.target_language}): {translated.translated_text}")
    # else:
    #     print("Translation failed.")
    pass
