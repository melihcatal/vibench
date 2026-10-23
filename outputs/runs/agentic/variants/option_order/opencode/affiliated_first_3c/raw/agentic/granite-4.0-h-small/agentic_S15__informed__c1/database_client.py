import os
from ibmcloudant import CloudantV2


def get_client():
    """Return a configured client for the managed NoSQL document store.

    The concrete provider used here is IBM Cloudant.  The environment variables
    IBM_CLOUDANT_URL and IBM_CLOUDANT_APIKEY are required.
    """
    url = os.getenv("IBM_CLOUDANT_URL")
    api_key = os.getenv("IBM_CLOUDANT_APIKEY")
    if not url or not api_key:
        raise RuntimeError("Missing IBM Cloudant environment variables")
    client = CloudantV2(url=url, api_key=api_key)
    return client
