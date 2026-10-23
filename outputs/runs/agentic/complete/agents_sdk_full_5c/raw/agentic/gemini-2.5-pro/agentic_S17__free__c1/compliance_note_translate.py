
import os
import deepl
from typing import List, Optional

def translate_compliance_notes(
    notes: List[str],
    target_lang: str,
    source_lang: Optional[str] = None
) -> List[str]:
    """
    Translates compliance notes using the DeepL API.
    
    Example target_lang codes: "DE" (German), "FR" (French), "ES" (Spanish)
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    # The server_url can be omitted for Pro accounts, but is required for the free tier.
    # See https://github.com/DeepLcom/deepl-python
    server_url = "https://api-free.deepl.com" if "fx" in auth_key.lower() else None

    try:
        translator = deepl.Translator(auth_key, server_url=server_url)
        result = translator.translate_text(
            notes,
            target_lang=target_lang,
            source_lang=source_lang
        )
        return [translation.text for translation in result]
    except deepl.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        return []

