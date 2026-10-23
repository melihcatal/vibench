from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from typing import Dict, Any, Optional


def fetch_document(db_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a document by its identifier from IBM Cloudant.
    Returns None if the document does not exist.
    """
    authenticator = IAMAuthenticator(os.getenv("IBM_CLOUDANT_APIKEY"))
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_CLOUDANT_URL"))

    try:
        response = client.get_document(db=db_name, doc_id=doc_id).get_result()
        return response
    except Exception as e:
        if "not found" in str(e).lower():
            return None
        raise e
