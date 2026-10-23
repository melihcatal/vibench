# Helper utilities for request/response shapes across providers

def normalize_request(text, source_lang, target_lang):
    """Return a provider-agnostic request dict.
    Override as needed per provider.
    """
    return {
        'text': text,
        'source_language': source_lang,
        'target_language': target_lang,
    }


def normalize_response(raw_response, source_lang, target_lang):
    """Convert provider-specific response to a uniform dict.",
    return {
        'translated_text': raw_response.get('translated_text', ''),
        'detected_source_language': raw_response.get('detected_source_language', source_lang),
    }
