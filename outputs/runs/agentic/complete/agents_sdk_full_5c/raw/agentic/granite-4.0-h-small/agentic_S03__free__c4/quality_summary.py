import os
import json
from translation_client import TranslationClient
from translation_models import summarize_quality

def generate_quality_summary(texts: List[str], source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate a list of texts and return a concise quality summary.
    Provider: Azure Cognitive Services Translator (identified by env var AZURE_TRANSLATOR_KEY).
    """
    client = TranslationClient()
    payload = [
        {'Text': t, 'SourceLanguage': source_lang, 'TargetLanguage': target_lang}
        for t in texts
    ]
    response = client._request(client.BATCH_PATH, payload)
    translations = json.loads(response)
    normalized = []
    for item in translations:
        translation = item.get('translations', [{}])[0]
        normalized.append({'source': item.get('text'), 'target': translation.get('text')})
    summary = summarize_quality(normalized)
    return json.dumps(summary, indent=2)

if __name__ == '__main__':
    demo = ['Hello', 'How are you?', 'Goodbye', '']
    print('Quality Summary:')
    print(generate_quality_summary(demo))