from google.cloud import translate

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def translate_platform_output(output: str, target_language: str) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{GOOGLE_APPLICATION_CREDENTIALS}/locations/global"
    response = client.translate_text(
        parent=parent, contents=[output], target_language_code=target_language
    )
    return response.translations[0].translated_text
