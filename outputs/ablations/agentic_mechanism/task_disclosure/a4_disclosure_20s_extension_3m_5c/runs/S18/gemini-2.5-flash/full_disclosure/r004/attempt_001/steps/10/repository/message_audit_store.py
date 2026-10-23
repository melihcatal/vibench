from google.cloud import datastore
import datetime

class MessageAuditStore:
    def __init__(self, project_id: str):
        self.client = datastore.Client(project=project_id)
        self.kind = "MessageRecord"

    def store_message_record(self, message_id: str, status: str, payload_hash: str, timestamp: datetime.datetime = None):
        if timestamp is None:
            timestamp = datetime.datetime.now(datetime.timezone.utc)

        key = self.client.key(self.kind, message_id)
        entity = datastore.Entity(key=key)
        entity.update({
            "message_id": message_id,
            "status": status,
            "payload_hash": payload_hash,
            "timestamp": timestamp
        })
        self.client.put(entity)
        return entity

    def get_message_record(self, message_id: str):
        key = self.client.key(self.kind, message_id)
        entity = self.client.get(key)
        return entity
