import os
from google.cloud import translate_v2 as translate

def translate_runbook_notes(text: str, target_language: str = 'en') -> str:
    """Translates secret-rotation runbook notes using Google Cloud Translation.

    Args:
        text (str): The runbook notes to translate.
        target_language (str, optional): The target language code (e.g., 'en', 'es', 'fr'). Defaults to 'en'.

    Returns:
        str: The translated text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or that the environment has been authenticated (e.g., `gcloud auth application-default login`)
    
    client = translate.Client()

    try:
        # The `translate_text` method can also detect the source language automatically.
        result = client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        raise RuntimeError(f"Error during translation with Google Cloud Translation: {e}")

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set up)
    # japanese_runbook = """
    # 秘密のローテーション手順：
    # 1. 新しい秘密を生成します。
    # 2. サービス設定を更新します。
    # 3. テストを実行します。
    # """
    # english_translation = translate_runbook_notes(japanese_runbook, target_language='en')
    # print(f"Original (Japanese):\n{japanese_runbook}")
    # print(f"Translated (English):\n{english_translation}")
    
    # spanish_notes = "Notas de auditoría: Se accedió a la clave de API por un usuario autorizado."
    # english_from_spanish = translate_runbook_notes(spanish_notes, target_language='en')
    # print(f"\nOriginal (Spanish):\n{spanish_notes}")
    # print(f"Translated (English):\n{english_from_spanish}")
    pass
