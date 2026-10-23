from typing import Dict, Any
import os
from ibmcloudant import CouchDBSession
from ibmcloudant.cloudant_v1 import CloudantV1

# IBM Cloudant for audit storage
IBM_CLOUDANT_URL = os.getenv("IBM_CLOUDANT_URL")
IBM_CLOUDANT_APIKEY = os.getenv("IBM_CLOUDANT_APIKEY")
IBM_CLOUDANT_DB = "federated_login_audit"


def login_audit_store(event: Dict[str, Any]) -> bool:
    """Persist federated-login audit records in IBM Cloudant."""
    client = CloudantV1.new_instance()
    client.set_service_url(IBM_CLOUDANT_URL)
    client.set_default_headers({"Authorization": f"Bearer {IBM_CLOUDANT_APIKEY}"})

    # Create database if it doesn't exist
    try:
        client.put_database(db=IBM_CLOUDANT_DB)
    except Exception:
        pass  # Database may already exist

    # Store audit event
    response = client.post_document(db=IBM_CLOUDANT_DB, document=event)

    return response.result.get("ok", False)
