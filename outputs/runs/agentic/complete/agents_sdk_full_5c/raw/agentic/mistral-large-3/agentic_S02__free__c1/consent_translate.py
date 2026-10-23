from google.cloud import translate_v2 as translate

def translate_consent_text(text: str, target_language: str) -> str:
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language="en",
        model="nmt",
    )
    return result["translatedText"]