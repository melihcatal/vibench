import os

from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def login_audit_store(record: dict) -> dict:
    authenticator = IAMAuthenticator(os.environ.get("IBM_CLOUDANT_APIKEY", ""))
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(os.environ.get("IBM_CLOUDANT_URL", ""))
    result = client.post_document(
        db=os.environ.get("IBM_CLOUDANT_DB", "login_audit"), document=record
    ).get_result()
    return result
