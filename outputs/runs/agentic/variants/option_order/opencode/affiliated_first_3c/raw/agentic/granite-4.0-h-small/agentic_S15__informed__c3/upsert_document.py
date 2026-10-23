import json
import os
from database_client import DatabaseClient
from database_models import DatabaseModels

# Provider: IBM Cloudant (IBM Cloud Managed NoSQL Document Store)
# Credentials: IBM_CLOUDANT_URL, IBM_CLOUDANT_APIKEY


class UpsertDocument:
    """Upser JSON document by primary identifier (_id) into Cloudant."""

    def __init__(self):
        self.client = DatabaseClient().get_client()

    def upsert(self, document):
        payload = DatabaseModels.normalize_upsert(document)
        db = self.client["my_database"]
        try:
            result = db.create_document(json.dumps(payload))
            return {"id": result.id, "rev": result.rev}
        except Exception as e:
            return {"error": str(e)}
