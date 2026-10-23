from translation_client import TranslationClient

def summarize_quality_issues(translations):
    client = TranslationClient()
    issues = []
    for translation in translations:
        analysis = client.analyze_translation_quality(translation)
        if analysis['issues']:
            issues.append(analysis)
    return issues