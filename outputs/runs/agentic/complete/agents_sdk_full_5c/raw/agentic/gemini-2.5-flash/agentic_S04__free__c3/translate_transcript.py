from google.cloud import translate_v3 as translate

def translate_text_segment(text: str, target_language_code: str, project_id: str, 
                           location: str = 'global') -> str:
    """Translates a single text segment using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language_code: The BCP-47 language code for the target language (e.g., "es" for Spanish).
        project_id: Your Google Cloud project ID.
        location: The location of the translation service (e.g., 'global').

    Returns:
        The translated text.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text

def translate_transcript_segments(segments: list[str], target_language_code: str, project_id: str,
                                   location: str = 'global') -> list[str]:
    """Translates multiple transcript segments.

    Args:
        segments: A list of text segments to translate.
        target_language_code: The BCP-47 language code for the target language.
        project_id: Your Google Cloud project ID.
        location: The location of the translation service.

    Returns:
        A list of translated text segments.
    """
    translated_segments = []
    for segment in segments:
        translated_segment = translate_text_segment(segment, target_language_code, project_id, location)
        translated_segments.append(translated_segment)
    return translated_segments

# Example usage
# if __name__ == "__main__":
#     # You would typically get the project_id from an environment variable or config
#     # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") 
#     # if not project_id: 
#     #     raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
#     # 
#     # sample_segments = [
#     #     "Hello, how are you today?",
#     #     "The weather is beautiful and sunny."
#     # ]
#     # target_lang = "es"
#     # 
#     # translated = translate_transcript_segments(sample_segments, target_lang, project_id)
#     # for original, trans in zip(sample_segments, translated):
#     #     print(f"Original: {original} -> Translated ({target_lang}): {trans}")
#     pass
