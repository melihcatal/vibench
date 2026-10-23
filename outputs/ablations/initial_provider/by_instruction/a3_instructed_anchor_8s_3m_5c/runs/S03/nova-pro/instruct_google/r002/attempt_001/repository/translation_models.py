from.translation_client import get_translation_client, location_path

def normalize_response(response):
    return response.translations[0].translated_text if response else None