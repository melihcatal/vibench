import os
from ibm_cos_sdk import Client

# Environment variables for IBM Cloud Object Storage
# IBM_COS_ENDPOINT, IBM_COS_APIKEY


def get_managed_storage_client():
    endpoint = os.getenv("IBM_COS_ENDPOINT")
    api_key = os.getenv("IBM_COS_APIKEY")
    if not endpoint or not api_key:
        raise RuntimeError(
            "Set IBM_COS_ENDPOINT and IBM_COS_APIKEY environment variables"
        )
    # The Client class handles credential loading internally
    return Client(endpoint=endpoint)
