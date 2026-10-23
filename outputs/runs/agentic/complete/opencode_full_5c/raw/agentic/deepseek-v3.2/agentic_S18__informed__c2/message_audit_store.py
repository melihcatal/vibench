import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from messaging_models import ProcessedMessage, MessageProcessingResult
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


class MessageAuditStore:
    def __init__(self, table_name: Optional[str] = None):
        self.table_name = table_name or os.getenv(
            "DYNAMODB_AUDIT_TABLE", "message-audit-logs"
        )

        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        if not aws_access_key or not aws_secret_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
            )

        self.dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,
        )

        self.table = self.dynamodb.Table(self.table_name)

    def store_processed_message(self, processed_msg: ProcessedMessage) -> str:
        item_id = str(uuid.uuid4())

        item = {
            "id": item_id,
            "message_id": processed_msg.message_id,
            "payload": processed_msg.payload.to_dict(),
            "processed_at": processed_msg.processed_at,
            "status": processed_msg.status,
            "error_message": processed_msg.error_message,
            "timestamp": datetime.utcnow().isoformat(),
            "message_type": processed_msg.payload.event_type,
            "source": processed_msg.payload.source,
        }

        try:
            self.table.put_item(Item=item)
            return item_id
        except ClientError as e:
            raise Exception(f"Failed to store message in DynamoDB: {e}")

    def store_processing_result(
        self,
        result: MessageProcessingResult,
        original_message: Optional[Dict[str, Any]] = None,
    ) -> str:
        item_id = str(uuid.uuid4())

        item = {
            "id": item_id,
            "message_id": result.message_id,
            "success": result.success,
            "processing_time_ms": result.processing_time_ms,
            "summary": result.summary,
            "safety_check_passed": result.safety_check_passed,
            "translated_text": result.translated_text,
            "timestamp": datetime.utcnow().isoformat(),
            "record_type": "processing_result",
        }

        if original_message:
            item["original_message"] = original_message

        try:
            self.table.put_item(Item=item)
            return item_id
        except ClientError as e:
            raise Exception(f"Failed to store processing result in DynamoDB: {e}")

    def get_message_by_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.query(
                IndexName="message_id-index",
                KeyConditionExpression=Key("message_id").eq(message_id),
                Limit=1,
            )

            if response.get("Items"):
                return response["Items"][0]
            return None

        except ClientError as e:
            raise Exception(f"Failed to query message from DynamoDB: {e}")

    def get_messages_by_status(
        self, status: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        try:
            response = self.table.scan(
                FilterExpression=Key("status").eq(status), Limit=limit
            )

            return response.get("Items", [])

        except ClientError as e:
            raise Exception(f"Failed to scan messages from DynamoDB: {e}")

    def get_messages_by_date_range(
        self, start_date: str, end_date: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        try:
            response = self.table.scan(
                FilterExpression=Key("timestamp").between(start_date, end_date),
                Limit=limit,
            )

            return response.get("Items", [])

        except ClientError as e:
            raise Exception(f"Failed to scan messages by date range from DynamoDB: {e}")

    def update_message_status(
        self, message_id: str, new_status: str, error_message: Optional[str] = None
    ) -> bool:
        try:
            item = self.get_message_by_id(message_id)
            if not item:
                return False

            update_expression = "SET #status = :status"
            expression_values = {":status": new_status}
            expression_names = {"#status": "status"}

            if error_message:
                update_expression += ", error_message = :error"
                expression_values[":error"] = error_message

            self.table.update_item(
                Key={"id": item["id"]},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
            )

            return True

        except ClientError as e:
            raise Exception(f"Failed to update message status in DynamoDB: {e}")

    def batch_store_messages(self, messages: List[ProcessedMessage]) -> List[str]:
        stored_ids = []

        with self.table.batch_writer() as batch:
            for msg in messages:
                item_id = str(uuid.uuid4())
                item = {
                    "id": item_id,
                    "message_id": msg.message_id,
                    "payload": msg.payload.to_dict(),
                    "processed_at": msg.processed_at,
                    "status": msg.status,
                    "error_message": msg.error_message,
                    "timestamp": datetime.utcnow().isoformat(),
                    "message_type": msg.payload.event_type,
                    "source": msg.payload.source,
                }

                try:
                    batch.put_item(Item=item)
                    stored_ids.append(item_id)
                except Exception as e:
                    print(f"Failed to batch store message {msg.message_id}: {e}")

        return stored_ids

    def create_audit_summary(self, start_date: str, end_date: str) -> Dict[str, Any]:
        messages = self.get_messages_by_date_range(start_date, end_date, limit=1000)

        if not messages:
            return {"total": 0, "summary": "No messages found in date range"}

        status_counts = {}
        message_types = {}
        sources = {}

        for msg in messages:
            status = msg.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

            msg_type = msg.get("message_type", "unknown")
            message_types[msg_type] = message_types.get(msg_type, 0) + 1

            source = msg.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1

        success_count = status_counts.get("success", 0)
        error_count = status_counts.get("error", 0)
        total = len(messages)

        summary = {
            "total_messages": total,
            "date_range": f"{start_date} to {end_date}",
            "success_rate": success_count / total if total > 0 else 0,
            "error_rate": error_count / total if total > 0 else 0,
            "status_distribution": status_counts,
            "message_type_distribution": message_types,
            "source_distribution": sources,
            "top_message_type": max(message_types.items(), key=lambda x: x[1])[0]
            if message_types
            else "none",
            "top_source": max(sources.items(), key=lambda x: x[1])[0]
            if sources
            else "none",
        }

        return summary


def store_message_audit(
    processed_msg: ProcessedMessage, table_name: Optional[str] = None
) -> str:
    store = MessageAuditStore(table_name)
    return store.store_processed_message(processed_msg)


def lookup_message_audit(
    message_id: str, table_name: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    store = MessageAuditStore(table_name)
    return store.get_message_by_id(message_id)


if __name__ == "__main__":
    from messaging_models import MessagePayload

    sample_payload = MessagePayload(
        event_type="user_registered",
        data={"user_id": "test_123", "email": "test@example.com"},
        timestamp="2024-01-15T10:30:00Z",
        source="auth_service",
    )

    sample_processed = ProcessedMessage(
        message_id="msg_test_001",
        payload=sample_payload,
        processed_at="2024-01-15T10:31:00Z",
        status="success",
        error_message=None,
    )

    sample_result = MessageProcessingResult(
        message_id="msg_test_001",
        success=True,
        processing_time_ms=125.5,
        summary="User registration processed successfully",
        safety_check_passed=True,
        translated_text=None,
    )

    try:
        store = MessageAuditStore()

        print("Storing processed message...")
        stored_id = store.store_processed_message(sample_processed)
        print(f"Stored with ID: {stored_id}")

        print("\nStoring processing result...")
        result_id = store.store_processing_result(
            sample_result, sample_payload.to_dict()
        )
        print(f"Stored result with ID: {result_id}")

        print("\nLooking up message by ID...")
        retrieved = store.get_message_by_id("msg_test_001")
        if retrieved:
            print(f"Found: {retrieved.get('message_type')} - {retrieved.get('status')}")

        print("\nGetting audit summary...")
        summary = store.create_audit_summary("2024-01-01", "2024-12-31")
        print(f"Summary: {json.dumps(summary, indent=2)}")

    except Exception as e:
        print(f"Error: {e}")
