from google.cloud import translate_v2 as translate


def translate_text(text, target_language="en"):
    translate_client = translate.Client.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
