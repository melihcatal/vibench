import os
from google.cloud import secretmanager


def get_client():
    return secretmanager.SecretManagerServiceClient()


def normalize_response(response):
    return response.payload.data.decode("UTF-8")
