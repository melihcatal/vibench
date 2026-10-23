from google.cloud import translate_v3 as translate


def translate_caption(text: str, target_language: str = "es") -> str:
    client = translate.TranslationServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your GCP Project ID
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""
