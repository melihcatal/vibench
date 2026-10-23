
from pymongo import MongoClient
import os
from document_models import ExpenseRecord

def validate_document_fields(expense_record: ExpenseRecord) -> dict:
    """
    Validates required structured fields and confidence scores against a MongoDB Atlas schema.
    This function simulates a check; direct schema validation typically happens at insertion.
    Here, we'll connect and ensure the connection works, and conceptualize the validation rules.
    """
    # MongoDB Atlas connection string (ensure sensitive info is handled securely, e.g., environment variables)
    MONGO_URI = os.getenv("MONGO_ATLAS_URI")
    DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "expenses_db")
    COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "expense_records")

    if not MONGO_URI:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")

    validation_results = {
        "is_valid": True,
        "errors": [],
        "confidence_scores_ok": True, # Placeholder for actual confidence score validation
    }

    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # Simulate checking collection schema (this isn't how direct field validation works with pymongo,
        # but represents the *intent* of using Atlas for schema enforcement).
        # In MongoDB Atlas, you'd define schema validation rules on the collection itself.
        # For programmatic checks, you'd define rules here.

        if not expense_record.vendor_name:
            validation_results["is_valid"] = False
            validation_results["errors"].append("Vendor name is missing.")
        if not expense_record.transaction_date:
            validation_results["is_valid"] = False
            validation_results["errors"].append("Transaction date is missing.")
        if expense_record.total_amount is None or expense_record.total_amount <= 0:
            validation_results["is_valid"] = False
            validation_results["errors"].append("Total amount is missing or invalid.")

        # For confidence scores, we'd ideally have these in ExpenseRecord and check against thresholds.
        # Since the provided schema doesn't have confidence scores, this is a placeholder logic.
        # E.g., if expense_record.confidence_score < 0.7: validation_results["confidence_scores_ok"] = False

    except Exception as e:
        validation_results["is_valid"] = False
        validation_results["errors"].append(f"Database connection or validation error: {e}")
    finally:
        if 'client' in locals():
            client.close()

    return validation_results

if __name__ == '__main__':
    # Example usage:
    from document_models import ExpenseRecord
    import json

    # Ensure MONGO_ATLAS_URI is set in your environment for this example to connect
    # os.environ["MONGO_ATLAS_URI"] = "mongodb+srv://<user>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority"
    # os.environ["MONGO_DATABASE_NAME"] = "test_expenses"
    # os.environ["MONGO_COLLECTION_NAME"] = "test_records"

    valid_expense = ExpenseRecord(
        document_type="invoice",
        vendor_name="Acme Corp",
        transaction_date="2023-10-26",
        total_amount=150.75,
        line_items=[{"description": "Widget A", "amount": 100.0, "quantity": 1}]
    )

    invalid_expense = ExpenseRecord(
        document_type="receipt",
        vendor_name="", # Missing
        transaction_date="2023-10-26",
        total_amount=-10.00, # Invalid
        line_items=[]
    )

    print("Validating valid expense:")
    # print(json.dumps(validate_document_fields(valid_expense), indent=2))

    print("
Validating invalid expense:")
    # print(json.dumps(validate_document_fields(invalid_expense), indent=2))
    print("Connect to MongoDB Atlas and configure schema validation for full effect.")
