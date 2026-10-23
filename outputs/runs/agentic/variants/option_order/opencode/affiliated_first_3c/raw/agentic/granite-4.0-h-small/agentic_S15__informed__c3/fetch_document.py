import json
import os
from database_client import DatabaseClient
from database_models import DatabaseModels

# Provider: IBM Cloudant (IBM Cloud Managed NoSQL Document Store)
# Credentials: IBM_CLOUDANT_URL, IBM_CLOUDANT_APIKEY


class FetchDocument:
    """Fetch a document by its _id from Cloudant."""

    def __init__(self):
        self.client = DatabaseClient().get_client()

    def fetch(self, doc_id):
        db = self.client["my_database"]
        try:
            doc = db.get_document(doc_id)
            return {"document": doc}
        except Exception as e:
            return {"error": str(e)}
