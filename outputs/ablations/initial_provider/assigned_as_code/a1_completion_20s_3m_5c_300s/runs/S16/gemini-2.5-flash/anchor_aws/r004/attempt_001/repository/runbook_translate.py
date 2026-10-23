from google.cloud import translate_v2 as translate


def runbook_translate(payload, config=None):
    config = config or {}
    client = translate.Client()
    text = payload["runbook_notes"]
    target_language = payload.get("target_language", "en")

    result = client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "original_text": result["input"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
