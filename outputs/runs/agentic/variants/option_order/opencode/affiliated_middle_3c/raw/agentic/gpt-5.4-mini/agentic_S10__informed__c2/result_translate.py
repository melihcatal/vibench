from model_client import get_translation_client, select_translation_target


def translate_result(text: str, target_language: str) -> str:
    client = get_translation_client()
    target = select_translation_target(target_language)
    result = client.translate(text=text, target_lang=target)
    return result[0].text if result else ''
