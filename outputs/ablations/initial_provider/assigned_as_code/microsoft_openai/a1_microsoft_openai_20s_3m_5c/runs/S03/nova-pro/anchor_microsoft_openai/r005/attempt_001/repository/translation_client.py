import os


def get_translation_config():
    return {
        'api_key': os.getenv('TRANSLATOR_API_KEY'),
        'region': os.getenv('TRANSLATOR_REGION')
    }


def create_translation_client():
    config = get_translation_config()
    return {
        'api_key': config['api_key'],
        'region': config['region']
    }