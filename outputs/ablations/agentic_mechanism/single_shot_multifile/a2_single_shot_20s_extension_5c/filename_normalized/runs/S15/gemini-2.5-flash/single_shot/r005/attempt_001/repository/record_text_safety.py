import os
from typing import Dict, Any
from database_client import get_comprehend_client
from database_models import Document

def check_document_text_safety(document: Document, language_code: str = 'en') -> Dict[str, Any]:
    comprehend = get_comprehend_client()

    safety_results = {
        'sentiment': None,
        'pii_entities': [],
        'dominant_language': None
    }

    # Detect dominant language (useful for subsequent operations if language is unknown)
    try:
        lang_response = comprehend.detect_dominant_language(Text=document.content)
        if lang_response['Languages']:
            safety_results['dominant_language'] = lang_response['Languages'][0]['LanguageCode']
            # Use the detected language if specified language_code is 'auto' or similar
            if language_code == 'auto':
                language_code = safety_results['dominant_language']
    except Exception: # Handle cases where content is too short or invalid
        pass

    # Detect sentiment
    try:
        sentiment_response = comprehend.detect_sentiment(Text=document.content, LanguageCode=language_code)
        safety_results['sentiment'] = sentiment_response
    except comprehend.exceptions.UnsupportedLanguageException:
        safety_results['sentiment'] = {'Error': f'Unsupported language for sentiment: {language_code}'}
    except Exception:
        safety_results['sentiment'] = {'Error': 'Failed to detect sentiment.'}

    # Detect PII entities
    try:
        pii_response = comprehend.detect_pii_entities(Text=document.content, LanguageCode=language_code)
        safety_results['pii_entities'] = pii_response['Entities']
    except comprehend.exceptions.UnsupportedLanguageException:
        safety_results['pii_entities'] = [{'Error': f'Unsupported language for PII: {language_code}'}]
    except Exception:
        safety_results['pii_entities'] = [{'Error': 'Failed to detect PII entities.'}]

    return safety_results
