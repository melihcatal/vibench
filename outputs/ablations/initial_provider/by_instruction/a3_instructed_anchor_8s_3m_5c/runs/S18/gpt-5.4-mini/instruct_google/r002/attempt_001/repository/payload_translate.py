from google.cloud import translate_v3 as translate


def payload_translate(text, target_language="en"):
    client = translate.TranslationServiceClient()
    response = client.translate_text(
        parent="projects/{}/locations/global".format(""),
        contents=[text],
        mime_type="text/plain",
        target_language_code=target_language,
    )
    return {"provider": "google-cloud-translate", "translated_text": response.translations[0].translated_text if response.translations else text}
