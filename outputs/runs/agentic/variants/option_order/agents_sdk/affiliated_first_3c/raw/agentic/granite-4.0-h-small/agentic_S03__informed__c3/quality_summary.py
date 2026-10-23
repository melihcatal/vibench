import os
from translation_models import parse_single_response, summarize_quality
from translation_client import get_translation_client
from ibm_watson import LanguageTranslatorV3

def analyze_translation_batch(original_texts: List[str], translated_texts: List[str]) -> List[Dict[str, Any]]:
    """Analyze a batch of translations and return quality summaries."""
    client = get_translation_client()
    summaries = []
    for orig, trans in zip(original_texts, translated_texts):
        # Example: we can call the provider's quality endpoint or reuse the parsed text.
        # Here we reuse the helper function that computes a simple overlap score.
        summary = summarize_quality(trans, orig)
        summaries.append(summary)
    return summaries

if __name__ == '__main__':
    sample = [
        'Hello, this is a test.',
        'Welcome to the platform.'
    ]
    client = get_translation_client()
    # Simple round-trip translation as a demo (could be actual translations)
    trans = [client.translate({'text': t, 'source':'en','target':'fr'}).get_result().get('translation','').get('translated_text','') for t in sample]
    summaries = analyze_translation_batch(sample, trans)
    print('Quality summaries:')
    for s in summaries:
        print(s)
