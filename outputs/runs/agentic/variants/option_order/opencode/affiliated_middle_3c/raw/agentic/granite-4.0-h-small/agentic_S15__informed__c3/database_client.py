# [HELPER] database_client.py
import os


def get_managed_client() -> object:
    """Return a pre-configured client for the selected Managed NoSQL Document Store.

    Configuration is read from environment variables. The concrete provider is selected
    via the SERVICE type environment variable. Example implementations for each supported
    provider are shown.
    """
    service = os.getenv("NO_SQL_SERVICE", "MongoDB_Atlas")
    if service == "MongoDB_Atlas":
        from pymongo import MongoClient

        uri = os.getenv("MONGODB_ATLAS_URI")
        return MongoClient(uri)
    elif service == "Azure_Cosmos_DB":
        from azure.cosmos import CosmosClient

        endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        key = os.getenv("AZURE_COSMOS_KEY")
        return CosmosClient(endpoint, credential=key)
    elif service == "IBM_Cloudant":
        from ibmcloudant.cloudant_v1 import CloudantV1

        url = os.getenv("IBM_CLOUDANT_URL")
        api_key = os.getenv("IBM_CLOUDANT_APIKEY")
        return CloudantV1(url, api_key=api_key)
    elif service == "Alibaba_Tablestore":
        from tablestore import SyncClient

        endpoint = os.getenv("ALIBABA_ENDPOINT")
        ak_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
        ak_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        return SyncClient(endpoint, access_key_id=ak_id, access_key_secret=ak_secret)
    elif service == "Google_Firestore":
        from google.cloud import firestore

        # Application Default Credentials
        return firestore.Client()
    elif service == "Amazon_DynamoDB":
        from boto3 import resource

        return resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))
    else:
        raise ValueError(f"Unsupported NO_SQL_SERVICE: {service}")


# Example: client = get_managed_client()
