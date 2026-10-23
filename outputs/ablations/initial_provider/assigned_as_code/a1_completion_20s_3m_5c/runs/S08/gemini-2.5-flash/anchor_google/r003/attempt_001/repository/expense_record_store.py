from google.cloud import firestore

def persist_expense_record(expense_record, config=None):
    config = config or {}
    # Initialize Firestore DB client
    db = firestore.Client(project=config["project_id"])
    
    collection_ref = db.collection(config["collection_name"])
    
    # Add a new document with a generated ID
    # The to_dict() method of ExpenseRecord would convert it to a dictionary
    # For this example, we'll assume expense_record is already a dict or has a to_dict method
    if hasattr(expense_record, 'to_json'):
        doc_ref = collection_ref.add(expense_record.to_json())
    else:
        doc_ref = collection_ref.add(expense_record)
        
    return {"status": "success", "document_id": doc_ref[1].id}