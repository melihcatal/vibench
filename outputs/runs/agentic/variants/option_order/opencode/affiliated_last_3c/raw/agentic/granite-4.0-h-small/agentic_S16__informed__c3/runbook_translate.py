import os
import json
import requests
from security_client import create_secrets_manager_client

# LATER-STEP: Translate secret-rotation runbook notes

def runbook_translate(runbook_text: str, target_lang: str = 'zh') -> str:
    """Translate a secret‑rotation runbook snippet to another language using DeepL.
    
    Returns the translated text.
    ">
    # DeepL API endpoint (free tier requires auth key)
    endpoint = 'https://api.deepl.com/v2/translate'
    params = {
        'auth_key': os.getenv('DEEPL_AUTH_KEY'),
        'text': runbook_text,
        'target_lang': target_lang
    }
    response = requests.post(endpoint, data=params)
    response.raise_for_status()
    result = response.json()
    return result['translations'][0]['text']

# Example usage
if __name__ == '__main__':
    sample = "Rotate the database secret weekly and record the new version in the audit log."
    translated = runbook_translate(sample, target_lang='zh')
    print('Translated runbook:', translated)
