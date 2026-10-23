import os
from google.cloud import datastore
from document_models import NormalizedExpense, LineItem
from typing import Dict, Any

def persist_expense_record(expense: NormalizedExpense, config=None) -> Dict[str, Any]:
    config = config or {}
    project_id = config.get("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT"))

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided.")

    client = datastore.Client(project=project_id)

    kind = "NormalizedExpenseRecord"
    name = f"{expense.document_type}-{expense.vendor_name}-{expense.transaction_date}-{expense.total_amount}"
    key = client.key(kind, name)

    entity = datastore.Entity(key=key)
    
    # Convert NormalizedExpense Pydantic model to a dictionary suitable for Datastore
    # Datastore does not directly support nested Pydantic models, so convert to dicts.
    expense_dict = expense.dict()
    
    # Convert line_items from list of LineItem models to list of dicts
    if expense_dict.get("line_items"):
        expense_dict["line_items"] = [item for item in expense_dict["line_items"]]

    entity.update(expense_dict)

    client.put(entity)
    return {"status": "success", "key": entity.key.path}
