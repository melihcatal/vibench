from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from typing import Dict, Any


def upsert_document(
    db_name: str, doc_id: str, document: Dict[str, Any], revision: str = None
) -> Dict[str, Any]:
    """
    Upserts a JSON document into IBM Cloudant by its primary identifier.
    If the document exists, it updates it; otherwise, it creates a new document.
    """
    authenticator = IAMAuthenticator(os.getenv("IBM_CLOUDANT_APIKEY"))
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_CLOUDANT_URL"))

    if revision:
        document["_rev"] = revision

    if doc_id in (None, ""):
        response = client.post_document(db=db_name, document=document).get_result()
    else:
        document["_id"] = doc_id
        try:
            response = client.put_document(
                db=db_name, doc_id=doc_id, document=document
            ).get_result()
        except Exception as e:
            if "not found" in str(e).lower():
                response = client.post_document(
                    db=db_name, document=document
                ).get_result()
            else:
                raise e

    return response
