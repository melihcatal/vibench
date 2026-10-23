import json
import os
from database_client import DatabaseClient
from database_models import DatabaseModels

# Provider: IBM Cloudant (IBM Cloud Managed NoSQL Document Store)
# Credentials: IBM_CLOUDANT_URL, IBM_CLOUDANT_APIKEY


class QueryDocuments:
    """Query Cloudant documents by field value or partition-style key."""

    def __init__(self):
        self.client = DatabaseClient().get_client()

    def query(self, filters):
        qfilter = DatabaseModels.normalize_query(filters)
        db = self.client["my_database"]
        # Simple GET /my_database/_find example for demonstration
        try:
            body = {"selector": qfilter, "limit": 100}
            # Cloudant python SDK uses session.get with JSON body
            import requests

            response = requests.post(
                f"{self.client.get_server_url()}/my_database/_find",
                json=body,
                auth=(os.getenv("IBM_CLOUDANT_APIKEY"), ""),
            )
            response.raise_for_status()
            return {"results": response.json().get("docs", [])}
        except Exception as e:
            return {"error": str(e)}
