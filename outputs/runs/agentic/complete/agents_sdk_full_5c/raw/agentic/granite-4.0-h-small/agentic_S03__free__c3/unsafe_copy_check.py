import os
from translation_client import get_client

def check_unsafe_content(translated_texts: list[str]) -> dict:
    """Check a list of translated strings for unsafe content using Google Cloud Content Filtering.",
    """
    client = get_client()
    unsafe = []
    safe = []
    for text in translated_texts:
        # Google Cloud Content Filtering endpoint (pseudo-code)
        result = client.check_content(content=text, category_configs=[{'enabled': True}])
        if result['unsafe']:
            unsafe.append(text)
        else:
            safe.append(text)
    return {'safe': safe, 'unsafe': unsafe