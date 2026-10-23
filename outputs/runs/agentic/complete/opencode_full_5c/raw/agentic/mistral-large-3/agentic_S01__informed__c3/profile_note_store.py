import os
from typing import Dict, Any
from ibmcloudant import CouchDbSessionAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1


class ProfileNoteStore:
    def __init__(self):
        authenticator = CouchDbSessionAuthenticator(
            os.getenv("IBM_CLOUDANT_URL"), os.getenv("IBM_CLOUDANT_APIKEY")
        )
        self.client = CloudantV1(authenticator=authenticator)
        self.db_name = os.getenv("IBM_CLOUDANT_DB_NAME", "onboarding_notes")

    def store_note(self, user_id: str, note: Dict[str, Any]) -> Dict[str, Any]:
        document = {
            "_id": f"note_{user_id}_{note.get('timestamp', '')}",
            "user_id": user_id,
            **note,
        }
        response = self.client.post_document(
            db=self.db_name, document=document
        ).get_result()
        return {"document_id": response["id"], "rev": response["rev"]}

    def get_notes(self, user_id: str) -> list:
        response = self.client.post_find(
            db=self.db_name, selector={"user_id": {"$eq": user_id}}
        ).get_result()
        return response.get("docs", [])


def profile_note_store(user_id: str, note: Dict[str, Any]) -> Dict[str, Any]:
    store = ProfileNoteStore()
    return store.store_note(user_id, note)
