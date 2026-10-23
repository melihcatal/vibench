import os
from azure.identity import DefaultAzureCredential

def get_identity_client():
    credential = DefaultAzureCredential()
    return credential
