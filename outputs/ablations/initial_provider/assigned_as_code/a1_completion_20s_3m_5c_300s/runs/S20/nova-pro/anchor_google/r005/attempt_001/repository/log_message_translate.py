import logging
from observability_client import ObservabilityClient

def translate_log_message(log_message, target_locale):
    client = ObservabilityClient()
    translated_message = client.translate(log_message, target_locale)
    logging.info(f'Translated log message: {translated_message}')
    return translated_message

if __name__ == '__main__':
    log_message = 'User login attempt'
    target_locale = 'es'
    translate_log_message(log_message, target_locale)