import os
from ibmcloudant import CloudantV2

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS

DATABASE_NAME = "login_audit"


class AuditStore:
    def __init__(self):
        url = os.getenv("CLOUDANT_URL")
        apikey = os.getenv("CLOUDANT_APIKEY")
        self.client = CloudantV2(service_url=url, api_key=apikey)
        self.db = self.client.get_database(DATABASE_NAME, create=True)

    def persist_event(self, event_doc: dict):
        # event_doc should contain _id or will be auto-generated
        self.db.create_document(event_doc)


if __name__ == "__main__":
    store = AuditStore()
    sample_event = {
        "_id": "evt-20230401-001",
        "user_id": "user123",
        "event_type": "login_success",
        "timestamp": "2023-04-01T12:00:00Z",
        "details": {"ip": "203.0.113.5"},
    }
    store.persist_event(sample_event)
