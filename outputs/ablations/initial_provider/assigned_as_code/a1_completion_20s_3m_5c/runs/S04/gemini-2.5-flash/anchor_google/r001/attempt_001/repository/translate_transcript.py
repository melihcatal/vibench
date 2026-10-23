from google.cloud import translate_v3 as translate

def translate_transcript(text_segments: list[str], target_language_code: str, project_id: str):
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    translated_segments = []
    for segment in text_segments:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [segment],
                "target_language_code": target_language_code,
            }
        )
        translated_segments.append(response.translations[0].translated_text)
    return translated_segments
