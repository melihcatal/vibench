# runbook_translate.py
# [LATER-STEP]
# Translate secret-rotation runbook notes using Azure Translator Text API
import json
from azure.ai.translation import TranslationClient
from azure.core.credentials import AzureKeyCredential
from security_client import ensure_credentials
from security_models import SecretRotationRequest, SecretRotationResponse

def translate_runbook(request: SecretRotationRequest, target_lang: str = 'fr') -> str:
    """Translate any notes attached to a rotation request into another language.",
    # Ensure Azure credentials are present
    ensure_credentials(provider='azure')
    client = TranslationClient(endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT'), credential=AzureKeyCredential(os.getenv('AZURE_TRANSLATOR_KEY')))
    translated = client.translate_text(request.get('notes', ''), to_language=target_lang)
    return translated.translations[0].text if translated.translations else ''

if __name__ == '__main__':
    sample_request: SecretRotationRequest = {
        'path': 'my-db-secret',
        'current_version': 'latest',
        'target_version': '3',
        'notes': 'Rotate the secret annually and store change logs in the audit log.',
    }
    print('Translated notes:', translate_runbook(sample_request))
