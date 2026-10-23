from google.cloud import kms
from google.cloud import logging
from google.cloud import dlp_v2
from google.cloud import translate_v3

def get_kms_client():
    return kms.KeyManagementServiceClient()

def get_logging_client():
    return logging.Client()

def get_dlp_client():
    return dlp_v2.DlpServiceClient()

def get_translate_client():
    return translate_v3.TranslationServiceClient()
