import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from google.cloud import firestore
from messaging_models import ProcessedMessage, EventMessage


class MessageAuditStore:
    def __init__(self, collection_name: str = "message_audit"):
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set for Google Firestore"
            )

        self.db = firestore.Client()
        self.collection_name = collection_name
        self.collection_ref = self.db.collection(collection_name)

    def store_processed_message(self, processed_message: ProcessedMessage) -> str:
        try:
            message_data = processed_message.to_dict()
            message_data["stored_at"] = datetime.utcnow().isoformat()
            message_data["provider"] = "Google Firestore"

            doc_ref = self.collection_ref.document(processed_message.message_id)
            doc_ref.set(message_data)

            print(
                f"Stored processed message {processed_message.message_id} in Google Firestore collection {self.collection_name}"
            )

            return doc_ref.id

        except Exception as e:
            print(f"Failed to store message in Google Firestore: {e}")
            raise

    def get_message_by_id(self, message_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc_ref = self.collection_ref.document(message_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                data["id"] = doc.id
                return data
            else:
                return None

        except Exception as e:
            print(f"Failed to retrieve message from Google Firestore: {e}")
            raise

    def query_messages(
        self, filters: Dict[str, Any], limit: int = 100
    ) -> list[Dict[str, Any]]:
        try:
            query = self.collection_ref

            for field, value in filters.items():
                if isinstance(value, (list, tuple)) and len(value) == 2:
                    op, val = value
                    if op == "==":
                        query = query.where(field, "==", val)
                    elif op == ">":
                        query = query.where(field, ">", val)
                    elif op == "<":
                        query = query.where(field, "<", val)
                    elif op == ">=":
                        query = query.where(field, ">=", val)
                    elif op == "<=":
                        query = query.where(field, "<=", val)
                else:
                    query = query.where(field, "==", value)

            query = query.limit(limit)
            results = query.stream()

            messages = []
            for doc in results:
                data = doc.to_dict()
                data["id"] = doc.id
                messages.append(data)

            print(
                f"Queried {len(messages)} messages from Google Firestore with filters: {filters}"
            )

            return messages

        except Exception as e:
            print(f"Failed to query messages from Google Firestore: {e}")
            raise

    def update_message_status(
        self,
        message_id: str,
        status: str,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> bool:
        try:
            doc_ref = self.collection_ref.document(message_id)
            doc = doc_ref.get()

            if not doc.exists:
                print(f"Message {message_id} not found in Google Firestore")
                return False

            update_data = {
                "status": status,
                "updated_at": datetime.utcnow().isoformat(),
            }

            if additional_data:
                update_data.update(additional_data)

            doc_ref.update(update_data)

            print(
                f"Updated message {message_id} status to {status} in Google Firestore"
            )

            return True

        except Exception as e:
            print(f"Failed to update message in Google Firestore: {e}")
            raise

    def store_batch_audit(
        self, batch_id: str, messages: list[ProcessedMessage]
    ) -> Dict[str, Any]:
        try:
            batch = self.db.batch()
            batch_doc_ref = self.collection_ref.document(f"batch_{batch_id}")

            batch_data = {
                "batch_id": batch_id,
                "total_messages": len(messages),
                "successful": sum(1 for m in messages if m.status == "success"),
                "failed": sum(1 for m in messages if m.status == "failed"),
                "processed_at": datetime.utcnow().isoformat(),
                "provider": "Google Firestore",
            }

            batch.set(batch_doc_ref, batch_data)

            for message in messages:
                message_doc_ref = self.collection_ref.document(message.message_id)
                message_data = message.to_dict()
                message_data["batch_id"] = batch_id
                message_data["stored_at"] = datetime.utcnow().isoformat()
                message_data["provider"] = "Google Firestore"

                batch.set(message_doc_ref, message_data)

            batch.commit()

            print(
                f"Stored batch {batch_id} with {len(messages)} messages in Google Firestore"
            )

            return batch_data

        except Exception as e:
            print(f"Failed to store batch audit in Google Firestore: {e}")
            raise


def create_sample_processed_message():
    event_message = EventMessage(
        event_type="user_login",
        payload={"user_id": "user_123", "action": "login", "ip": "192.168.1.1"},
        timestamp=datetime.utcnow().isoformat(),
        source="auth_service",
        correlation_id="corr_001",
    )

    return ProcessedMessage(
        message_id="msg_001",
        event_message=event_message,
        processed_at=datetime.utcnow().isoformat(),
        status="success",
        processing_duration_ms=150,
        summary="User login processed successfully",
        safety_score=0.1,
    )


if __name__ == "__main__":
    try:
        store = MessageAuditStore()

        sample_message = create_sample_processed_message()

        print("Storing sample message...")
        doc_id = store.store_processed_message(sample_message)
        print(f"Stored with ID: {doc_id}")

        print("\nRetrieving message...")
        retrieved = store.get_message_by_id(sample_message.message_id)
        if retrieved:
            print(
                f"Retrieved: {retrieved['event_message']['event_type']} - {retrieved['status']}"
            )

        print("\nQuerying messages by status...")
        messages = store.query_messages({"status": "success"}, limit=5)
        print(f"Found {len(messages)} successful messages")

        print("\nUpdating message status...")
        updated = store.update_message_status(
            sample_message.message_id,
            "archived",
            {"archived_at": datetime.utcnow().isoformat()},
        )
        print(f"Updated: {updated}")

    except Exception as e:
        print(f"Error: {e}")
