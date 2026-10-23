from document_client import DocumentClient


def translate_text(text: str, target_language: str = "en") -> str:
    client = DocumentClient()

    # The target language for translation
    result = client.translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
