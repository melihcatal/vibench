import os
from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Dict, Any


class ProfileNoteStore:
    def __init__(self):
        authenticator = IAMAuthenticator(os.getenv("IBM_CLOUDANT_APIKEY"))
        self.client = CloudantV1(authenticator=authenticator)
        self.client.set_service_url(os.getenv("IBM_CLOUDANT_URL"))
        self.db_name = "onboarding_notes"

    def store_profile_note(self, user_id: str, note: Dict[str, Any]) -> Dict[str, Any]:
        document = {"_id": user_id, **note}
        response = self.client.post_document(
            db=self.db_name, document=document
        ).get_result()
        return response