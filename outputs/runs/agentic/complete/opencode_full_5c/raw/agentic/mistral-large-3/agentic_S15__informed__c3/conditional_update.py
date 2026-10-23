from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from typing import Dict, Any, Optional


def conditional_update(
    db_name: str,
    doc_id: str,
    update_function: callable,
    condition_field: str = None,
    condition_value: Any = None,
) -> Optional[Dict[str, Any]]:
    """
    Applies a conditional or version-aware update to a document in IBM Cloudant.
    The update_function must accept the current document and return the updated document.
    If condition_field and condition_value are provided, the update only applies if the field matches the value.
    """
    authenticator = IAMAuthenticator(os.getenv("IBM_CLOUDANT_APIKEY"))
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(os.getenv("IBM_CLOUDANT_URL"))

    # Fetch the current document
    try:
        doc = client.get_document(db=db_name, doc_id=doc_id).get_result()
    except Exception as e:
        if "not found" in str(e).lower():
            return None
        raise e

    # Check condition if provided
    if condition_field and condition_value is not None:
        if doc.get(condition_field) != condition_value:
            return None

    # Apply the update function
    updated_doc = update_function(doc)
    if not updated_doc:
        return None

    # Perform the update
    response = client.put_document(
        db=db_name, doc_id=doc_id, document=updated_doc
    ).get_result()

    return response
