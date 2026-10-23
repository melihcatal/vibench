from google.cloud import translate_v2 as translate


def record_translate(record: dict, target_language: str = "en") -> dict:
    client = translate.Client()
    translated = {}
    for key, value in record.items():
        if isinstance(value, str):
            translated[key] = client.translate(value, target_language=target_language).get("translatedText", value)
        else:
            translated[key] = value
    return translated
