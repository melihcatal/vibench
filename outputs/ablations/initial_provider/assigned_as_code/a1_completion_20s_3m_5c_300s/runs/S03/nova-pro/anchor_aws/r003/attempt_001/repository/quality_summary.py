import os
from google.cloud import translate_v2 as translate

def summarize_quality_issues(translations):
    client = translate.Client()
    issues = []
    for translation in translations:
        result = client.translate(translation, target_language='en')
        if result['detectedSourceLanguage']!= 'en':
            issues.append(f'Potential mistranslation: {translation}')
    return issues