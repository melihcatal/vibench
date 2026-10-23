import os
from ibmcloudant.cloudant_v1 import CloudantV1

os.environ["IBM_CLOUDANT_URL"] = "your-cloudant-url"
os.environ["IBM_CLOUDANT_APIKEY"] = "your-cloudant-apikey"


def store_note(note):
    client = CloudantV1.iam_service(
        url=os.getenv("IBM_CLOUDANT_URL"), api_key=os.getenv("IBM_CLOUDANT_APIKEY")
    )
    document = {"type": "note", "content": note}
    response = client.post_document(db="onboarding-notes", document=document)
    return response.get_result()
