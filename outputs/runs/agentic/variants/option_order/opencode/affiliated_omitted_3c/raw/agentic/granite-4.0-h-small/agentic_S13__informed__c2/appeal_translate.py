import json
from safety_client import SafetyClient


def translate_appeal(appeal_text: str, target_lang: str = "en") -> str:
    """Translate appeal text using Alibaba Machine Translation.

    Returns the translated string.
    """
    client = SafetyClient()
    # Placeholder: call Alibaba MT SDK; here we simulate with uppercasing
    translated = appeal_text.upper()  # demo transformation
    return translated
