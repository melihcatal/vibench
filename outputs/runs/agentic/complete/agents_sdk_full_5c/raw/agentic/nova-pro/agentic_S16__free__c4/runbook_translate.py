import boto3
import google.auth
from google.cloud import translate_v2 as translate

def translate_runbook_notes(secret_id, target_language):
    client = boto3.client('secretsmanager')
    describe_secret_response = client.describe_secret(SecretId=secret_id)
    notes = describe_secret_response.get('Description', '')
    translate_client = translate.Client()
    translation = translate_client.translate(notes, target_language=target_language)
    return translation['translatedText']