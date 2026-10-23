from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient
from google.cloud import logging_v2
from google.cloud import dlp_v2
from google.cloud import aiplatform
from google.cloud import translate


def get_key_vault_cryptography_client(key_id: str) -> CryptographyClient:
    credential = DefaultAzureCredential()
    return CryptographyClient(key_id, credential=credential)

def get_gcp_logging_client():
    return logging_v2.Client()

def get_gcp_dlp_client():
    return dlp_v2.DlpServiceClient()

def get_gcp_aiplatform_prediction_client(project: str, location: str):
    return aiplatform.gapic.PredictionServiceClient(client_options={'api_endpoint': f'{location}-aiplatform.googleapis.com'})

def get_gcp_translate_client():
    return translate.TranslationServiceClient()
