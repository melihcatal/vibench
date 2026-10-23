import json
import os
from database_client import DatabaseClient
from database_models import DatabaseModels

# Provider: IBM Cloudant (IBM Cloud Managed NoSQL Document Store)
# Credentials: IBM_CLOUDANT_URL, IBM_CLOUDANT_APIKEY


class ConditionalUpdate:
    """Apply a conditional/version-aware update to a document in Cloudant."""

    def __init__(self):
        self.client = DatabaseClient().get_client()

    def update(self, doc_id, update_payload, version):
        doc = DatabaseModels.normalize_conditional_update(
            doc_id, update_payload, version
        )
        db = self.client["my_database"]
        try:
            # Cloudant uses rev field for conditional updates
            result = db.update_document(json.dumps(doc))
            return {"id": result.id, "rev": result.rev}
        except Exception as e:
            return {"error": str(e)}
