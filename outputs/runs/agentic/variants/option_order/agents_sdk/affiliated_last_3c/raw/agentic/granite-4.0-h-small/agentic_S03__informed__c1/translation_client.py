import os
from google.cloud import translate_v2 as translate

class TranslationClient:
    def __init__(self):
        # CLIENT is created once and reused; credentials loaded from env var
        self.client = translate.Client()

    def translate_text(self, text, target_language='es'):
        return self.client.translate(text, target_language=target_language)['translatedText']

    def batch_translate(self, texts, target_language='es'):
        # Preserve order using list comprehension
        return [self.translate_text(t, target_language) for t in texts]

if __name__ == '__main__':
    client = TranslationClient()
    print(client.translate_text('Hello', 'fr'))