import os
from typing import Dict, Any, Optional

# Load environment variables for Managed NoSQL Document Store
MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
AZURE_COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT")
AZURE_COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY")
ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


# Simple client factory returning provider‑specific client instance
def get_database_client(provider: str) -> Any:
    """Return a ready‑to‑use client from the requested provider.

    provider: one of
        - "mongodb"
        - "azure"
        - "alibaba"
        - "google"
        - "dynamodb"
    """
    if provider == "mongodb":
        import pymongo

        return pymongo.MongoClient(MONGODB_ATLAS_URI)
    elif provider == "azure":
        from azure.cosmos import CosmosClient, exceptions

        client = CosmosClient(AZURE_COSMOS_ENDPOINT, key=AZURE_COSMOS_KEY)
        return client  # client or specific database/client can be created later
    elif provider == "alibaba":
        import tablestore

        return tablestore.Client(
            endpoint="https://your-instance.cn-hangzhou.ots.aliyuncs.com",
            accessKeyId=ALIBABA_CLOUD_ACCESS_KEY_ID,
            accessKeySecret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
        )
    elif provider == "google":
        from google.cloud import firestore

        return firestore.Client()
    elif provider == "dynamodb":
        import boto3

        return boto3.resource(
            "dynamodb",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")
