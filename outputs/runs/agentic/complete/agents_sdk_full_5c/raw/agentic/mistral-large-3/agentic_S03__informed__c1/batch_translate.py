from typing import List
from translation_client import AmazonTranslateClient
from translation_models import (
    batch_requests_from_list,
    batch_responses_to_list,
    normalize_language_code
)


def batch_translate(texts: List[str], source_lang: str, target_lang: str) -> List[str]:
    """Translate a list of strings using Amazon Translate while preserving order."""
    client = AmazonTranslateClient()
    source_lang = normalize_language_code(source_lang)
    target_lang = normalize_language_code(target_lang)
    
    requests = batch_requests_from_list(texts, source_lang, target_lang)
    responses = []
    
    for req in requests:
        translated_text = client.translate_text(req["text"], req["source_lang"], req["target_lang"])
        responses.append({
            "translated_text": translated_text if translated_text else "",
            "source_lang": req["source_lang"],
            "target_lang": req["target_lang"]
        })
    
    return batch_responses_to_list(responses)