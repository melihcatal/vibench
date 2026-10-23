import os

from azure.identity import DefaultAzureCredential

# [HELPER] observability_client.py


def get_credentials():
    return DefaultAzureCredential()


def get_resource_uri():
    return os.getenv("AZURE_MONITOR_RESOURCE_URI")
