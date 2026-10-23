# security_client.py
# Local configuration and client helper utilities for Secret Management
import os


def get_secret_manager_client():
    # Example for Google Cloud Secret Manager
    from google.cloud import secretmanager

    return secretmanager.SecretManagerServiceClient()


def get_doppler_client():
    import requests

    return requests.Session()


def get_ibm_secrets_manager_client(apikey):
    from ibm_secrets_manager_sdk import SecretsManagerV2

    return SecretsManagerV2(iam_apikey=apikey)
