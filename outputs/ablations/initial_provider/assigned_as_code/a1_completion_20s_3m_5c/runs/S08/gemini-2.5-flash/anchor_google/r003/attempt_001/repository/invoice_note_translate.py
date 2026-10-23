from google.cloud import translate_v2 as translate

def translate_invoice_notes(text_content, target_language='en', config=None):
    config = config or {}
    translate_client = translate.Client()

    # The Google Cloud Translation API client automatically handles project ID and authentication
    # using credentials configured in the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS)

    result = translate_client.translate(
        text_content,
        target_language=target_language
    )

    return {
        "original_text": text_content,
        "translated_text": result['translatedText'],
        "source_language": result['detectedSourceLanguage']
    }