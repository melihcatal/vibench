from typing import Union
from security_client import get_translate_client


def translate_compliance_note(
    note: Union[str, bytes], target_language_code: str
) -> str:
    client = get_translate_client()
    text = note.decode("utf-8") if isinstance(note, bytes) else str(note)
    response = client.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language_code
    )
    return response["TranslatedText"]
