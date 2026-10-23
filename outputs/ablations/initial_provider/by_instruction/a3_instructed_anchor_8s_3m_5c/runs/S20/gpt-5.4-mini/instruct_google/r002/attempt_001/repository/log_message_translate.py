from google.cloud import translate_v3


def translate_message(text: str, target_language_code: str = "es") -> str:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{client.project_path.split('/')[1]}/locations/global" if hasattr(client, "project_path") else "projects/unknown/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text if response.translations else text


if __name__ == "__main__":
    translate_message("example")
