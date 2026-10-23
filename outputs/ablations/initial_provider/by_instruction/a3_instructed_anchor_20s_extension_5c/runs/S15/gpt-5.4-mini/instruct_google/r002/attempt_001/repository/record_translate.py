from google.cloud import translate_v2 as translate


def record_translate(text, target_language="en"):
    client = translate.Client()
    return client.translate(text or "", target_language=target_language)
