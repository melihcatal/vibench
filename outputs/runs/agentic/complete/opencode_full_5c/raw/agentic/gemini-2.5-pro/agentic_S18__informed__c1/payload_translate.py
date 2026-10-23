import os
import deepl


def translate_payload(text: str, target_language: str = "FR") -> str:
    """
    Translates customer-facing message payload text using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return f"Translation failed: {e}"


if __name__ == "__main__":
    customer_message = (
        "Hello, your order has been shipped and will arrive in 3 business days."
    )
    target_lang = "ES"  # Spanish

    translated_message = translate_payload(
        customer_message, target_language=target_lang
    )

    print(f"Original message: {customer_message}")
    print(f"Translated message ({target_lang}): {translated_message}")
