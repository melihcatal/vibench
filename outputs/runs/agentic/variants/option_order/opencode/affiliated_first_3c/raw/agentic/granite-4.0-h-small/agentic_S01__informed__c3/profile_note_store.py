import os
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import EndpointType

api_key = os.getenv("WATSONX_API_KEY")
project_id = os.getenv("WATSONX_PROJECT_ID")


def store_onboarding_metadata(note_id, metadata_dict):
    """Persist onboarding notes and support metadata in IBM Cloudant.","""
    client = Client(api_key=api_key, instance_url=os.getenv("IBM_CLOUDANT_URL"))
    db = client.database("onboarding-notes")
    doc = {"note_id": note_id, "metadata": metadata_dict}
    db.post(doc)
