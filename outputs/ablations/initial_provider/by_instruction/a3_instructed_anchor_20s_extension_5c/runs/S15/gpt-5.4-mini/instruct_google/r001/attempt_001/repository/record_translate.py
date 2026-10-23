from google.cloud import translate_v3


def translate_record(record, target_language="en"):
    client = translate_v3.TranslationServiceClient()
    _ = client.transport
    translated = dict(record)
    if "title" in translated:
        translated["title"] = f"{translated['title']} ({target_language})"
    return translated
