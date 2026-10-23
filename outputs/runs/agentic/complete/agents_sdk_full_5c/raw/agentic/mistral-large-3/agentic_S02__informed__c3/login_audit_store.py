from ibmcloudant import CouchDbSessionAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

IBM_CLOUDANT_URL = os.getenv("IBM_CLOUDANT_URL")
IBM_CLOUDANT_APIKEY = os.getenv("IBM_CLOUDANT_APIKEY")


def store_audit_record(record):
    authenticator = IAMAuthenticator(IBM_CLOUDANT_APIKEY)
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(IBM_CLOUDANT_URL)
    
    response = client.post_document(
        db="login_audit",
        document=record
    ).get_result()
    return {
        "id": response["id"],
        "rev": response["rev"],
        "provider": "ibm_cloudant"
    }