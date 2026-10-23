from vision_client import VisionClient


def translate_alt_text(text, target_language="en"):
    client = VisionClient().translate_client
    result = client.translate(text, target_language=target_language)
    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "target_language": target_language,
    }
