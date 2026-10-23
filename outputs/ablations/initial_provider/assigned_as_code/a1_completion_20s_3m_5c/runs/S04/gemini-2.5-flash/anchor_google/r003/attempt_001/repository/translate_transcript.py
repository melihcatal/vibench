from google.cloud import translate_v2 as translate

def translate_transcript(text_segments: list[str], target_language_code: str):
    translate_client = translate.Client()
    translations = []
    for segment in text_segments:
        result = translate_client.translate(segment, target_language=target_language_code)
        translations.append(result["translatedText"])
    return {
        "source_segments": text_segments,
        "translated_segments": translations,
        "target_language": target_language_code,
    }
