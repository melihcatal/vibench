from vision_client import VisionClient
from vision_models import normalize_translation_response

def translate_alt_text(text: str, target_language: str = "es") -> str:
    client_helper = VisionClient()
    gct_client = client_helper.get_gct_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        return ""

    parent = f"projects/{project_id}/locations/global"

    try:
        response = gct_client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        # The response object from google-cloud-translate is not a dict directly compatible with model_dump()
        # We need to manually extract the translated text.
        if response.translations:
            return response.translations[0].translated_text
        return ""

    except Exception as e:
        print(f"Error translating alt text: {e}")
        return ""
