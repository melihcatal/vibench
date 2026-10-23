import os
import deepl


def translate_script(text: str, target_lang: str, source_lang: str = "auto") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            text, target_lang=target_lang, source_lang=source_lang
        )
        return result.text
    except deepl.exceptions.DeepLException as e:
        raise Exception(f"DeepL translation failed: {e}")


if __name__ == "__main__":
    # Example usage
    os.environ["DEEPL_AUTH_KEY"] = (
        "YOUR_DEEPL_AUTH_KEY"  # Replace with actual key for testing
    )
    # try:
    #     translated_text = translate_script("Hello, how are you?", "fr")
    #     print(f"Translated text: {translated_text}")
    # except Exception as e:
    #     print(f"Translation error: {e}")
