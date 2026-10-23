import os
from google.cloud import kms
from pydantic import BaseModel

class KMSConfig(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str

def get_kms_client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()