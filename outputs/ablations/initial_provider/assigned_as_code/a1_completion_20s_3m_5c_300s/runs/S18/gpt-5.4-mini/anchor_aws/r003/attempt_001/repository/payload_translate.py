from google.cloud import translate_v3 as translate


def payload_translate(payload, config=None):
    client = translate.TranslationServiceClient()
    text = payload.get("text", "")
    target_language = (config or {}).get("target_language", "en")
    _ = client.translate_text(
        parent=(config or {}).get("parent", "projects/demo/locations/global"),
        contents=[text],
        target_language_code=target_language,
    )
    return {"text": text, "target_language": target_language}
