import os


def get_translation_config():
    return {
        'api_key': os.getenv('MICROSOFT_TRANSLATOR_API_KEY'),
        'region': os.getenv('MICROSOFT_TRANSLATOR_REGION')
    }


def get_translation_client():
    config = get_translation_config()
    return {
        'api_key': config['api_key'],
        'region': config['region']
    }