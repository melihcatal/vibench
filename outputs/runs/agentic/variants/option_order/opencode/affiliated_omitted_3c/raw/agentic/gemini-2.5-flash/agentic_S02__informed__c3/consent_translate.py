import os
import deepl


def translate_consent_copy(text: str, target_lang: str = "en") -> str:
    """Translates identity-provider consent copy using the DeepL API."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    # The source language is automatically detected by DeepL
    result = translator.translate_text(text, target_lang=target_lang)

    return result.text


# Example usage (not part of the file, just for demonstration):
# if __name__ == "__main__":
#     os.environ["DEEPL_AUTH_KEY"] = "YOUR_DEEPL_AUTH_KEY"
#     sample_consent_text = "Durch die Nutzung dieser Dienste stimmen Sie unseren Allgemeinen Geschäftsbedingungen zu."
#     try:
#         translated_text = translate_consent_copy(sample_consent_text, target_lang="en")
#         print(f"Original (German): {sample_consent_text}")
#         print(f"Translated (English): {translated_text}")
#     except ValueError as e:
#         print(f"Configuration Error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
