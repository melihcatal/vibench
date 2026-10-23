from vision_client import get_translate_client
from vision_models import ImageDescription


def translate_description(
    description: ImageDescription, target_language: str = "es"
) -> str:
    client = get_translate_client()

    result = client.translate(description.text, target_language=target_language)

    return result["translatedText"]
