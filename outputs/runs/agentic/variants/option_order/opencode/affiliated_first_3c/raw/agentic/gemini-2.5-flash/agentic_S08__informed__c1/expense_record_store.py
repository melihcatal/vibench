from document_client import DocumentClient
from document_models import NormalizedExpense


def persist_expense_record(expense: NormalizedExpense) -> str:
    client = DocumentClient()
    db = client.firestore_client
    collection_ref = db.collection(client.firestore_collection_name)

    # Convert Pydantic model to a dictionary suitable for Firestore
    # pydantic_encoder doesn't handle datetime objects directly for Firestore
    expense_dict = expense.model_dump()
    if expense_dict.get("transaction_date"):
        # Convert date to string for Firestore if it's a datetime.date object
        expense_dict["transaction_date"] = expense_dict["transaction_date"].isoformat()

    # Add a new document with a generated ID
    doc_ref = collection_ref.add(expense_dict)
    return doc_ref[1].id  # Return the ID of the newly created document
