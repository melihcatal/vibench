from.translation_client import translation_client

def quality_summary(text, target_language):
    client = translation_client()
    translation = client.translate(text, target_language=target_language, timeout=30)
    quality_issues = {
        'original': text,
        'translated': translation['translatedText'],
        'issues': 'Placeholder for quality issues'
    }
    return quality_issues