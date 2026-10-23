import os
import json
import boto3
from datetime import datetime
from messaging_models import DeadLetterPayload, PublishRequest


class DynamoDBMessageStore:
    """
    Persists processed messages (both successful and dead-lettered) to DynamoDB.
    """

    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def _make_pk(self, msg_id: str, timestamp: int) -> str:
        return f"MSG#{msg_id}#{timestamp}"

    def put_success(self, req: PublishRequest, processed_at: datetime):
        """
        Store a successfully processed message.
        """
        pk = self._make_pk(
            req.payload.get("id", "unknown"), int(processed_at.timestamp())
        )
        item = {
            "PK": pk,
            "type": "success",
            "original_topic": req.topic,
            "payload": json.dumps(req.payload),
            "processed_at": processed_at.isoformat(),
        }
        self.table.put_item(Item=item)

    def put_dead_letter(
        self,
        original_topic: str,
        msg_key: str,
        raw_msg: str,
        error: str,
        processed_at: datetime,
    ):
        """
        Store a message that ended up in the dead letter queue.
        """
        pk = self._make_pk(
            str(msg_key) if msg_key else "unknown", int(processed_at.timestamp())
        )
        item = {
            "PK": pk,
            "type": "dead_letter",
            "original_topic": original_topic,
            "key": msg_key,
            "raw_message": raw_msg,
            "error": error,
            "processed_at": processed_at.isoformat(),
        }
        self.table.put_item(Item=item)

    @staticmethod
    def get(cls, table_name: str, pk: str):
        """
        Retrieve a processed record from DynamoDB.
        """
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
        resp = table.get_item(Key={"PK": pk})
        return resp.get("Item")


# ---------------------------------------------------------------------------
# Example usage (run locally after setting env vars and creating the table)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    table_name = os.getenv("DYNAMODB_TABLE")
    if not table_name:
        raise RuntimeError("DYNAMODB_TABLE environment variable not set")
    store = DynamoDBMessageStore(table_name)
    # Example put
    demo_req = PublishRequest(topic="demo", payload={"text": "audit test", "id": "123"})
    store.put_success(demo_req, datetime.now())
