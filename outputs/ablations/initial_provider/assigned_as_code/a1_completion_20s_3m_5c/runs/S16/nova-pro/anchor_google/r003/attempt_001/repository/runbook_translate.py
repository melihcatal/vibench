from google.cloud import translate_v2 as translate


def runbook_translate(payload, config=None):
    config = config or {}
    client = translate.Client(config)
    translation = client.translate(payload['runbook_note'], target_language=payload['target_language'])
    return {'translated_note': translation['translatedText']}