from typing import Dict, Any, List
from document_models import NormalizedExpense

def validate_document_fields(expense_record: NormalizedExpense, required_fields: List[str]) -> Dict[str, Any]:
    """
    Validates required structured fields in a normalized expense record.
    Returns a dictionary indicating validity and missing fields.
    """
    validation_results = {"is_valid": True, "missing_fields": [], "validation_errors": []}

    record_dict = expense_record.model_dump()

    for field in required_fields:
        field_path = field.split('.')
        current_value = record_dict
        found = True
        for part in field_path:
            if isinstance(current_value, dict) and part in current_value and current_value[part] is not None:
                current_value = current_value[part]
            else:
                found = False
                break
        
        # Special handling for numerical fields which might be 0.0 but considered valid
        if found and isinstance(current_value, (float, int)) and current_value == 0.0:
            pass # Valid if it's explicitly 0
        elif not found or (isinstance(current_value, str) and not current_value.strip()):
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)
            validation_results["validation_errors"].append(f"Missing or empty required field: {field}")

    # Add more complex validation logic here if needed, e.g., date format, amount ranges
    if not isinstance(expense_record.total_amount, (int, float)) or expense_record.total_amount < 0:
        validation_results["is_valid"] = False
        validation_results["validation_errors"].append("Total amount is invalid.")

    if expense_record.line_items:
        for i, item in enumerate(expense_record.line_items):
            if not item.description.strip():
                validation_results["is_valid"] = False
                validation_results["validation_errors"].append(f"Line item {i+1} has no description.")
            if not isinstance(item.amount, (int, float)) or item.amount < 0:
                validation_results["is_valid"] = False
                validation_results["validation_errors"].append(f"Line item {i+1} has an invalid amount.")

    return validation_results

if __name__ == '__main__':
    from datetime import date
    # Example Usage
    valid_expense = NormalizedExpense(
        document_type="invoice",
        vendor_name="Acme Corp",
        transaction_date="2023-01-15",
        total_amount=123.45,
        tax_amount=10.00,
        line_items=[
            LineItem(description="Widget A", quantity=1.0, unit_price=100.00, amount=100.00),
            LineItem(description="Service B", quantity=1.0, unit_price=23.45, amount=23.45)
        ]
    )
    required_invoice_fields = ["vendor_name", "transaction_date", "total_amount", "line_items"]
    validation_result_valid = validate_document_fields(valid_expense, required_invoice_fields)
    print("Validation Result (Valid):", validation_result_valid)

    print("\n"+"-"*30+"\n")

    invalid_expense = NormalizedExpense(
        document_type="receipt",
        vendor_name="", # Missing field
        transaction_date="",
        total_amount=-50.00, # Invalid amount
        tax_amount=0.00,
        line_items=[
            LineItem(description="", quantity=1.0, unit_price=50.00, amount=50.00) # Missing description
        ]
    )
    required_receipt_fields = ["vendor_name", "total_amount", "line_items.0.description"]
    validation_result_invalid = validate_document_fields(invalid_expense, required_receipt_fields)
    print("Validation Result (Invalid):", validation_result_invalid)
