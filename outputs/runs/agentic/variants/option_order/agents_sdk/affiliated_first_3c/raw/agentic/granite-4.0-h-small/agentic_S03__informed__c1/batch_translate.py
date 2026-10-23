# [SAME-SCENARIO] batch_translate.py

from typing import List, Dict
from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

def batch_translate(texts: List[str], source_lang: str = 'en', target_lang: str = 'es') -> List[str]:
    """Translate a list of strings while preserving order using a concrete provider.

    Uses Google Cloud Translation batch API (or multiple synchronous calls if batch is not supported).
    Credentials expected via GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = TranslationClient()
    # Group texts into batches of 128 (Google limit)
    batch_size = 128
    results: List[str] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        requests = [TranslationRequest(model_id="general", source_lang=source_lang, target_lang=target_lang, source_text=t) for t in batch]
        responses: List[TranslationResponse] = client.translate_batch(requests)
        results.extend(resp.translated_text for resp in responses)
    return results

# Example usage (removed in production)
#if __name__ == "__main__":
#    samples = ["Hello", "World", "How are you?"]
#    print(batch_translate(samples))
