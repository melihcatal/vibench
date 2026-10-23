import os
from google.cloud import translate_v2 as translate

class Normalizer:
    """Utility to standardize request/response fields for Translation API."""
    @staticmethod
    def normalize_request(text, target_language='es'):
        return {
            'q': text,
            'target': target_language
        }

    @staticmethod
    def normalize_response(raw):
        return raw.get('translatedText', '')

if __name__ == '__main__':
    norm = Normalizer()
    req = norm.normalize_request('Hello')
    print('Request dict:', req)
    # Manual demo using client directly since Normalizer does not invoke API
    client = translate.Client()
    print('Demo translation:', client.translate(req['q'], target_language=req['target']))