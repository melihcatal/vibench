import os
import requests

class TranslationClient:
    def __init__(self, config=None):
        self.config = config or {}
        self.api_key = self.config.get('api_key', os.getenv('TRANSLATOR_API_KEY'))
        self.region = self.config.get('region', os.getenv('TRANSLATOR_REGION'))

    def translate_text(self, payload):
        response = requests.post('https://api.cognitive.microsofttranslator.com/translate',
            headers={'Ocp-Apim-Subscription-Key': self.api_key,
                     'Ocp-Apim-Subscription-Region': self.region},
            params={'api-version': '3.0', 'from': payload['source_language'], 'to': payload['target_language']},
            json=[{'Text': payload['text']}], timeout=30)
        response.raise_for_status()
        return {'text': response.json()[0]['translations'][0]['text'],
                'source_language': payload['source_language'], 'target_language': payload['target_language']}