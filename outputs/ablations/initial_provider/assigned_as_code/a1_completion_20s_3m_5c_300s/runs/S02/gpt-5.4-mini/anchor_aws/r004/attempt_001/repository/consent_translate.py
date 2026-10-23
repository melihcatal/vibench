from google.cloud import translate_v3 as translate


def consent_translate(payload, config=None):
    client = translate.TranslationServiceClient()
    parent = f"projects/{(config or {}).get('google_cloud_project')}/locations/global"
    response = client.translate_text(
        parent=parent,
        contents=[payload["text"]],
        mime_type="text/plain",
        target_language_code=payload["target_language"],
    )
    return {"translated_text": response.translations[0].translated_text}
