from typing import Dict, List


def normalize_request(text: str, source_lang: str, target_lang: str) -> Dict:
    return {
        "Text": text,
        "SourceLanguageCode": source_lang,
        "TargetLanguageCode": target_lang,
    }


def normalize_response(response: Dict) -> str:
    return response["TranslatedText"]
