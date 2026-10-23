from translation_client import TranslationClient
from translation_models import normalize_dict_values


def translate_dictionary_values(data, source_language: str, target_language: str):
    client = TranslationClient()
    normalized = normalize_dict_values(data)
    payload = [{'Text': value} for value in normalized.values()]
    response = client.post('/translate', params={'api-version': '3.0', 'from': source_language, 'to': target_language}, json=payload)
    response.raise_for_status()
    translated = response.json()
    return {key: translated[index]['translations'][0]['text'] for index, key in enumerate(normalized.keys())}
