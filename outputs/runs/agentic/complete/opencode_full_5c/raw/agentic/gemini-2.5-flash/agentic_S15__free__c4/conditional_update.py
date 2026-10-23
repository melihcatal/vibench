from google.cloud import firestore
from google.cloud.firestore_v1.field_filter import FieldFilter
from database_client import get_db_client
from database_models import UpdateCondition


def conditional_update(
    collection_name: str, document_id: str, updates: dict, condition: UpdateCondition
):
    """Applies a conditional or version-aware update to one stored document in Firestore."""
    db = get_db_client()
    doc_ref = db.collection(collection_name).document(document_id)

    # For a true conditional update, Firestore transactions are generally preferred for atomicity.
    # Here, we'll simulate a simple conditional check based on a field value.
    # Firestore's update method itself can also take a pre-condition, but FieldFilter is more flexible.

    try:
        # Check the condition first. In a real-world scenario, especially for complex conditions
        # or atomicity, you'd use a transaction.
        doc = doc_ref.get()
        if not doc.exists:
            return {
                "id": document_id,
                "status": "failed",
                "reason": "Document not found",
            }

        current_value = doc.get(condition.field)
        condition_met = False
        if condition.operator == "==":
            condition_met = current_value == condition.value
        elif condition.operator == "!=":
            condition_met = current_value != condition.value
        elif condition.operator == ">":
            condition_met = current_value > condition.value
        elif condition.operator == "<":
            condition_met = current_value < condition.value
        # Add more operators as needed

        if condition_met:
            doc_ref.update(updates)
            return {"id": document_id, "status": "updated", "condition_met": True}
        else:
            return {
                "id": document_id,
                "status": "no_update",
                "condition_met": False,
                "reason": "Condition not met",
            }
    except Exception as e:
        return {"id": document_id, "status": "failed", "reason": str(e)}
