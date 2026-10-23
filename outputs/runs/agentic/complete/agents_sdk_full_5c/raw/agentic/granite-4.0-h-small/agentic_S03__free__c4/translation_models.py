import json
from typing import List, Dict, Any

def normalize_translation_response(response: str) -> List[Dict[str, Any]]:
    """Convert raw JSON response from Azure Translator into a normalized list of translations.
    Keeps only the translated text and the original source text.
    """
    data = json.loads(response)
    normalized = []
    for item in data:
        # Each item may contain multiple translations; keep the first
        translation = item.get('translations', [{}])[0]
        normalized.append({
            'source_text': item.get('text'),
            'target_text': translation.get('text', '')
        })
    return normalized

def summarize_quality(translations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Very simple quality summary: count of successful translations vs errors.
    In a real system you could plug in BLEU, METEOR, or custom heuristics.
    """
    summary = {
        'total': len(translations),
        'successful': 0,
        'errors': []
    }
    for t in translations:
        if t['target_text']:
            summary['successful'] += 1
        else:
            summary['errors'].append({'source': t['source_text'], 'reason': 'empty target'})
    return summary

def check_unsafe_content(texts: List[str]) -> List[bool]:
    """Placeholder for unsafe content detection.
    In production you would call a moderation API (e.g., Azure Content Safety) and return True if safe.
    """
    # Here we assume all inputs are safe for demonstration
    return [True] * len(texts)

if __name__ == '__main__':
    # Demo usage (remove in production)
    sample_resp = '[{"text":"Hello","translations":[{"text":"Hola"}]}]'
    print('Normalized:', normalize_translation_response(sample_resp))
    print('Quality:', summarize_quality(normalize_translation_response(sample_resp)))