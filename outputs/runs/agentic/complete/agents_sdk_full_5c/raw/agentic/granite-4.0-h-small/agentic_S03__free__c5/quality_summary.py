import json
from typing import List
from translation_models import denormalize_response
from translation_client import TranslationClient

CLIENT = TranslationClient.from_env()

TEXT_LIST = [
    {"text": "Hello world", "source_lang": "en", "target_lang": "es"},
    {"text": "Goodbye!", "source_lang": "en", "target_lang": "fr"},
]

responses = CLIENT.translate(texts=[t['text'] for t in TEXT_LIST],
                             source_languages=[t['source_lang'] for t in TEXT_LIST],
                             target_languages=[t['target_lang'] for t in TEXT_LIST])
print('Raw responses:', responses)
print('Quality summaries:')
for resp in responses:
    summary = denormalize_response(resp)
    # Example: flag empty translations as quality issue
    issues = []
    if not summary['translatedText']:
        issues.append('empty_translation')
    print(json.dumps({**summary, 'issues': issues}, indent=2))
