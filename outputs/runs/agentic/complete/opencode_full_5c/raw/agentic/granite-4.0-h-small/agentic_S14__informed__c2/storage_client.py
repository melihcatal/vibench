import os
from typing import Any, Dict


class StorageClient:
    """Local configuration and client helper utilities for Managed Object Storage.\n\n    Provides a unified interface to instantiate SDK clients for various providers.\n    The concrete provider is identified by environment variables specific to each service.\n"""

    PROVIDERS = {
        "backblaze_b2": {
            "sdk": "b2sdk",
            "env": ["B2_APPLICATION_KEY_ID", "B2_APPLICATION_KEY"],
        },
        "alibaba_oss": {
            "sdk": "oss2",
            "env": ["ALIBABA_CLOUD_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
        },
        "ibm_cos": {
            "sdk": "ibm-cos-sdk",
            "env": ["IBM_COS_ENDPOINT", "IBM_COS_APIKEY"],
        },
        "google_cloud": {
            "sdk": "google-cloud-storage",
            "env": ["GOOGLE_APPLICATION_CREDENTIALS"],
        },
        "azure_blob": {
            "sdk": "azure-storage-blob",
            "env": [
                "AZURE_STORAGE_ACCOUNT_NAME",
                "AZURE_STORAGE_ACCOUNT_KEY",
            ],
        },
        "amazon_s3": {
            "sdk": "boto3",
            "env": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        },
    }

    @staticmethod
    def get_provider_name() -> str:
        """Identify which provider is configured based on environment variables.\n\n        Returns the canonical name used in the PROVIDERS map, or raises ValueError.\n"""
        for name, cfg in StorageClient.PROVIDERS.items():
            if all(var in os.environ for var in cfg["env"]):
                return name
        raise ValueError(
            "No supported storage provider configured via environment variables"
        )
