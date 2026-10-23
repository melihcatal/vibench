from google.cloud import translate

def summarize_translation_quality_issues(original_text: str, translated_text: str, source_language: str, target_language: str) -> str:
    """
    Summarizes translation quality issues by re-translating the translated text back to the source language
    and comparing it with the original. Uses Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()

    # Re-translate the translated text back to the source language
    parent = f"projects/{{YOUR_PROJECT_ID}}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [translated_text],
            "source_language_code": target_language,
            "target_language_code": source_language,
        }
    )

    back_translated_text = response.translations[0].translated_text

    if original_text.lower() == back_translated_text.lower():
        return "No significant quality issues detected based on back-translation."
    else:
        return (
            f"Potential quality issues detected. Original: '{original_text}', "
            f"Back-translated: '{back_translated_text}'."
        )
