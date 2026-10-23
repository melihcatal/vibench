from typing import List, Dict, Any

def normalize_request(text: str, source_lang: str, target_lang: str, model_id: str = 'en-fr') -> Dict[str, Any]:
    """Create a provider‑specific payload for a single translation request."""
    return {
        'text': text,
        'source': source_lang,
        'target': target_lang,
        'model_id': model_id
    }

def normalize_batch_request(texts: List[str], source_lang: str, target_lang: str, model_id: str = 'en-fr') -> Dict[str, Any]:
    """Create a batch translation payload for a list of texts."""
    return {
        'texts': texts,
        'source': source_lang,
        'target': target_lang,
        'model_id': model_id
    }

def parse_single_response(resp: Dict[str, Any]) -> str:
    """Extract the translated text from a single translation response dict."""
    return resp.get('translation', '').get('translated_text', '')

def parse_batch_response(resp_list: List[Dict[str, Any]]) -> List[str]:
    """Return a list of translated texts preserving input order."""
    return [parse_single_response(item) for item in resp_list]

def summarize_quality(translation: str, original: str) -> Dict[str, Any]:
    """Placeholder that could be expanded to analyze translation quality.
    Currently returns a dummy score based on word overlap.
    """
    original_words = set(original.lower().split())
    translation_words = set(translation.lower().split())
    overlap = len(original_words & translation_words) / max(len(original_words), 1)
    return {
        'translation': translation,
        'original': original,
        'quality_score': round(float(overlap), 3)
    }
