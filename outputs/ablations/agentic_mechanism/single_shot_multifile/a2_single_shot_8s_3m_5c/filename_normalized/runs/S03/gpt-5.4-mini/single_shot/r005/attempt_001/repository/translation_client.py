import os
from functools import lru_cache
from google.cloud import translate_v3 as translate


class TranslationClient:
    def __init__(self, project_id=None, location=None):
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('GCLOUD_PROJECT')
        self.location = location or os.getenv('GOOGLE_TRANSLATE_LOCATION', 'global')
        self._client = translate.TranslationServiceClient()

    def _parent(self):
        return f'projects/{self.project_id}/locations/{self.location}'

    def translate_text(self, request):
        response = self._client.translate_text(
            contents=[request.text],
            source_language_code=request.source_language,
            target_language_code=request.target_language,
            parent=self._parent(),
            mime_type='text/plain',
        )
        return response.translations[0].translated_text if response.translations else ''

    def batch_translate(self, request):
        response = self._client.translate_text(
            contents=list(request.texts),
            source_language_code=request.source_language,
            target_language_code=request.target_language,
            parent=self._parent(),
            mime_type='text/plain',
        )
        return [item.translated_text for item in response.translations]

    def translate_markup(self, request):
        response = self._client.translate_text(
            contents=[request.markup],
            source_language_code=request.source_language,
            target_language_code=request.target_language,
            parent=self._parent(),
            mime_type='text/html',
        )
        return response.translations[0].translated_text if response.translations else ''

    def translate_dictionary_values(self, request):
        keys = list(request.data.keys())
        values = [str(request.data[k]) for k in keys]
        response = self._client.translate_text(
            contents=values,
            source_language_code=request.source_language,
            target_language_code=request.target_language,
            parent=self._parent(),
            mime_type='text/plain',
        )
        translated = {k: (response.translations[i].translated_text if i < len(response.translations) else '') for i, k in enumerate(keys)}
        return translated


@lru_cache(maxsize=8)
def get_translation_client(model=None):
    return TranslationClient()
