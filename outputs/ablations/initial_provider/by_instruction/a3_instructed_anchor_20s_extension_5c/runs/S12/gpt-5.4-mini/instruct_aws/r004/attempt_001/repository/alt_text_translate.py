import os

from vision_models import VisionResult


def alt_text_translate(text: str, target_language: str = "es") -> VisionResult:
    import google.cloud.translate_v2 as translate

    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return VisionResult(provider="google.cloud.translate_v2", kind="translation", source=os.getenv("SOURCE_LANGUAGE", "auto"), data={"translated_text": result.get("translatedText", ""), "target_language": target_language})
