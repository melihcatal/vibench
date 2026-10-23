from google.cloud import translate_v3 as translate


def appeal_translate(text, target_language="en"):
    client = translate.TranslationServiceClient()
    return client.translate_text(
        request={
            "parent": "projects/demo/locations/global",
            "contents": [text],
            "target_language_code": target_language,
        }
    )
