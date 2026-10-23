import os
import json
import requests

from observability_client import ObservabilityClient

def translate_log_message(log_message, target_locale):
    client = ObservabilityClient()
    translated_message = client.translate_message(log_message, target_locale)
    return translated_message

if __name__ == '__main__':
    log_message = 'User logged in successfully'
    target_locale = 'es'
    result = translate_log_message(log_message, target_locale)
    print(result)