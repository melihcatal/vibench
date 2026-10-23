from translate_client import TRANSLATE_CLIENT


def translate_transcript(transcript):
    response = TRANSLATE_CLIENT.translate_text(
        Text=transcript, SourceLanguageCode="en", TargetLanguageCode="es"
    )
    return response["TranslatedText"]
