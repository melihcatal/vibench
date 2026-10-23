import os
import deepl

def translate_invoice_note(text: str, target_lang: str = "en") -> str:
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not deepl_auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(deepl_auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.exceptions.DeepLException as e:
        print(f"Error translating text with DeepL API: {e}")
        return "Translation failed."

if __name__ == '__main__':
    # Example usage:
    # note_fr = "Merci pour votre paiement rapide de la facture."
    # translated_note_en = translate_invoice_note(note_fr, target_lang="en-US")
    # print(f"Original (FR): '{note_fr}'")
    # print(f"Translated (EN-US): '{translated_note_en}'")
    #
    # note_de = "Dies ist ein wichtiger Hinweis zur Rechnung."
    # translated_note_es = translate_invoice_note(note_de, target_lang="es")
    # print(f"Original (DE): '{note_de}'")
    # print(f"Translated (ES): '{translated_note_es}'")
    pass
