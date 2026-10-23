from database_client import get_firestore_client
from database_models import ConditionalUpdate
from google.cloud.firestore import Client
from google.cloud.firestore_v1.base_exceptions import ConflictError


def conditional_update(update_data: ConditionalUpdate, client: Client = None, project_id: str = None) -> bool:
    client = client or get_firestore_client(project_id=project_id)
    doc_ref = client.collection(update_data.collection).document(update_data.id)

    try:
        @firestore.transactional
        def update_in_transaction(transaction, doc_ref, update_data):
            snapshot = doc_ref.get(transaction=transaction)
            if not snapshot.exists:
                raise ValueError("Document does not exist.")

            current_data = snapshot.to_dict()
            if current_data.get("version") != update_data.current_version:
                raise ConflictError("Document version mismatch. Concurrent modification detected.")

            new_data = {
                **current_data,
                **update_data.updates,
                "version": update_data.new_version
            }
            transaction.set(doc_ref, new_data)
            return True

        transaction = client.transaction()
        return update_in_transaction(transaction, doc_ref, update_data)
    except ConflictError as e:
        print(f"Conditional update failed due to version mismatch: {e}")
        return False
    except ValueError as e:
        print(f"Conditional update failed: {e}")
        return False

