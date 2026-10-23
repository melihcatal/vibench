import os
import deepl


def translate_dashboard_note(text: str, target_locale: str) -> str:
    """
    Translates a dashboard note to the target locale using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        # The deepl.Translator class is the main entry point for the SDK.
        translator = deepl.Translator(auth_key)

        # The target_lang parameter expects locale codes like "EN-US", "DE", etc.
        result = translator.translate_text(text, target_lang=target_locale)

        if isinstance(result, deepl.TextResult):
            return result.text
        # Handle list of results if input text was a list
        elif isinstance(result, list) and result:
            return result[0].text
        else:
            return "Translation failed to produce a result."

    except deepl.DeepLException as e:
        return f"An error occurred with the DeepL API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
