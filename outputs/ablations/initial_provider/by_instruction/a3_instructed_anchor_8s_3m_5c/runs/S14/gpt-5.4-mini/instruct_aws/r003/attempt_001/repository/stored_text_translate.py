from typing import Optional

from storage_client import get_translate_client


def stored_text_translate(text: str, target_language_code: str, source_language_code: str = "auto", region: Optional[str] = None) -> str:
    translate = get_translate_client(region)
    response = translate.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return response["TranslatedText"]
