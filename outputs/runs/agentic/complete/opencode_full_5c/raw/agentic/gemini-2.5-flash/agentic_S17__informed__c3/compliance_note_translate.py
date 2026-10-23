from google.cloud import translate_v2 as translate
import os


def translate_compliance_notes(text: str, target_language: str = "en") -> str:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    translate_client = translate.Client()

    response = translate_client.translate(text, target_language=target_language)

    return response["translatedText"]


if __name__ == "__main__":
    # Example compliance note in Spanish
    spanish_note = "Nota de cumplimiento: La clave de cifrado ha sido rotada según la política de seguridad."

    try:
        translated_note = translate_compliance_notes(spanish_note, target_language="en")
        print(f"Original (Spanish): {spanish_note}")
        print(f"Translated (English): {translated_note}")

        # Example in German
        german_note = "Verschlüsselungsprotokoll: Die Daten wurden erfolgreich mit AES-256 verschlüsselt."
        translated_german_note = translate_compliance_notes(
            german_note, target_language="en"
        )
        print(f"Original (German): {german_note}")
        print(f"Translated (English): {translated_german_note}")

    except Exception as e:
        print(f"Error translating compliance notes: {e}")
