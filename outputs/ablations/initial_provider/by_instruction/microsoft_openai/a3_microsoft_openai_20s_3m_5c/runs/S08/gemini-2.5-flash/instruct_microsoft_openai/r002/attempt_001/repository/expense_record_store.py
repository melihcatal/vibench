from document_client import DocumentClients
from document_models import NormalizedExpense
import uuid

def persist_expense_record(expense_record: NormalizedExpense) -> str:
    clients = DocumentClients()
    if not clients.cosmos_container:
        raise ValueError("Azure Cosmos DB client not initialized or container not configured.")

    if not expense_record.transaction_id:
        expense_record.transaction_id = str(uuid.uuid4())

    # Convert dataclass to dictionary for Cosmos DB
    item = expense_record.__dict__
    # Convert line_items from list of LineItem dataclasses to list of dicts
    if item.get("line_items"):
        item["line_items"] = [li.__dict__ for li in item["line_items"]]

    # Cosmos DB requires 'id' field for document identification
    item["id"] = expense_record.transaction_id

    clients.cosmos_container.create_item(body=item)

    return expense_record.transaction_id
