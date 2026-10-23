import os
from datetime import datetime
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def profile_note_store(
    user_id: str, note_type: str, content: dict, metadata: dict = None
) -> dict:
    """Persist onboarding notes and support metadata in IBM Cloudant."""
    service_url = os.environ.get("IBM_CLOUDANT_URL")
    api_key = os.environ.get("IBM_CLOUDANT_APIKEY")

    if not service_url or not api_key:
        raise ValueError(
            "IBM_CLOUDANT_URL and IBM_CLOUDANT_APIKEY environment variables must be set"
        )

    authenticator = IAMAuthenticator(api_key)
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(service_url)

    db_name = "onboarding_notes"

    document = Document(
        id=f"{user_id}_{note_type}_{datetime.utcnow().isoformat()}",
        user_id=user_id,
        note_type=note_type,
        content=content,
        metadata=metadata or {},
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )

    try:
        response = client.post_document(db=db_name, document=document.to_dict())

        return {
            "id": response.result["id"],
            "rev": response.result["rev"],
            "user_id": user_id,
            "note_type": note_type,
            "created_at": document.created_at,
            "stored_in": "IBM Cloudant",
        }
    except Exception as e:
        raise Exception(f"Failed to store profile note in IBM Cloudant: {str(e)}")


def get_profile_notes(user_id: str, note_type: str = None, limit: int = 10) -> list:
    """Retrieve profile notes for a user from IBM Cloudant."""
    service_url = os.environ.get("IBM_CLOUDANT_URL")
    api_key = os.environ.get("IBM_CLOUDANT_APIKEY")

    if not service_url or not api_key:
        raise ValueError(
            "IBM_CLOUDANT_URL and IBM_CLOUDANT_APIKEY environment variables must be set"
        )

    authenticator = IAMAuthenticator(api_key)
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(service_url)

    db_name = "onboarding_notes"

    selector = {"user_id": user_id}
    if note_type:
        selector["note_type"] = note_type

    try:
        response = client.post_find(
            db=db_name, selector=selector, limit=limit, sort=[{"created_at": "desc"}]
        )

        return [doc for doc in response.result.get("docs", [])]
    except Exception as e:
        raise Exception(f"Failed to retrieve profile notes from IBM Cloudant: {str(e)}")
