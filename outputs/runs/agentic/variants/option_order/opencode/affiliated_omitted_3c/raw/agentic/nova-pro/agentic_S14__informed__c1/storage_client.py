import os
from b2sdk.v1 import B2Api, InMemoryAccountInfo


def get_b2_api():
    b2_info = InMemoryAccountInfo()
    b2_api = B2Api(b2_info)
    application_key_id = os.getenv("B2_APPLICATION_KEY_ID")
    application_key = os.getenv("B2_APPLICATION_KEY")
    b2_api.authorize_account("production", application_key_id, application_key)
    return b2_api
