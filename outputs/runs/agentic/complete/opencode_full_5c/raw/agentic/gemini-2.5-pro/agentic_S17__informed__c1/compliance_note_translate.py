from google.cloud import translate_v2 as translate
import os


def translate_note(note: str, target_language: str = "en") -> str:
    """
    Translates a given compliance note to the target language.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS not set.")

    translate_client = translate.Client()

    if isinstance(note, bytes):
        note = note.decode("utf-8")

    result = translate_client.translate(note, target_language=target_language)
    return result["translatedText"]
