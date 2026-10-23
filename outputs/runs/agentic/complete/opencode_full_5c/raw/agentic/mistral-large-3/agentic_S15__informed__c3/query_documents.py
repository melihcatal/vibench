from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from typing import Dict, Any, List


def query_documents(
    db_name: str, field_name: str, field_value: Any, partition_key: str = None
) -> List[Dict[str, Any]]:
    """
    Queries documents by a field value or partition-style key in IBM Cloudant.
    """
    authenticator = IAMAuthenticator(os.getenv("IBM_CLOUDANT_APIKEY"))
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_CLOUDANT_URL"))

    selector = {field_name: {"$eq": field_value}}
    if partition_key:
        selector["partition_key"] = {"$eq": partition_key}

    response = client.post_find(db=db_name, selector=selector).get_result()

    return response.get("docs", [])
