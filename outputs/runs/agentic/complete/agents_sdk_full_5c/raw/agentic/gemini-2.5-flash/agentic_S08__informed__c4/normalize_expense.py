from document_models import ExpenseDocument

def normalize_expense_data(expense_doc: ExpenseDocument) -> ExpenseDocument:
    """Normalizes extracted expense fields into a standard JSON schema. """
    # The ExpenseDocument model itself serves as the normalized schema.
    # Additional normalization logic can be added here if needed, 
    # e.g., mapping different vendor names to a single canonical name.
    return expense_doc
