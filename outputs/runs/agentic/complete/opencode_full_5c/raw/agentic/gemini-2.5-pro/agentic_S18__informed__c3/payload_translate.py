import os
import deepl


def translate_payload(text: str, target_language: str = "FR") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_language)
    return result.text


if __name__ == "__main__":
    customer_message = "Hello, I would like to know the status of my order."
    target_lang_code = "ES"  # Spanish

    print(f"Original: {customer_message}")
    translated_message = translate_payload(customer_message, target_lang_code)
    print(f"Translated to {target_lang_code}: {translated_message}")
