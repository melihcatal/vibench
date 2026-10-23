from google.cloud import translate_v2 as translate
from typing import Union, List


def translate_script(script: Union[str, List[str]], target_language: str = "es") -> str:
    client = translate.Client()
    text = " ".join(script) if isinstance(script, list) else script
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
