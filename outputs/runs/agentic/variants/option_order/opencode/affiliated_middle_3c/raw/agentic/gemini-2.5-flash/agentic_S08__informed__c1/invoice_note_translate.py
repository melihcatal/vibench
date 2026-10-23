import os
import deepl


def translate_invoice_notes(text_to_translate: str, target_lang: str = "EN") -> str:
    """
    Translates extracted invoice notes or descriptions using DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text_to_translate, target_lang=target_lang)

    return result.text


if __name__ == "__main__":
    # Placeholder for actual usage with DEEPL_AUTH_KEY set
    if not os.environ.get("DEEPL_AUTH_KEY"):
        print("Please set DEEPL_AUTH_KEY environment variable.")
    else:
        sample_note_german = "Dies ist eine Testnotiz für die Rechnung."
        sample_note_spanish = "Nota para la factura, por favor pague a tiempo."

        # translated_english = translate_invoice_notes(sample_note_german, target_lang="EN")
        # print("Translated to English (from German):", translated_english)

        # translated_english_from_spanish = translate_invoice_notes(sample_note_spanish, target_lang="EN")
        # print("Translated to English (from Spanish):", translated_english_from_spanish)
        print("DeepL API client configured for invoice note translation.")
