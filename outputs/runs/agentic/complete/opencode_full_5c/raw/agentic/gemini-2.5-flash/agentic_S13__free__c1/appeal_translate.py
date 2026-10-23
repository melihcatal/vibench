import os
from safety_client import GoogleSafetyClient


def translate_appeal_text(
    text: str, target_language_code: str, source_language_code: str = "en"
) -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get(
        "GOOGLE_CLOUD_LOCATION", "global"
    )  # Translation is often global

    client = GoogleSafetyClient(project_id, location)

    response = client.translate_client.translate_text(
        request={
            "parent": f"projects/{project_id}/locations/{location}",
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    return translated_text
