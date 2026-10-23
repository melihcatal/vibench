from document_models import NormalizedExpense


class ValidationError(Exception):
    pass


def validate_document_fields(expense: NormalizedExpense):
    if not expense.vendor:
        raise ValidationError("Vendor information is missing.")
    if not expense.total:
        raise ValidationError("Total amount is missing.")

    # Placeholder for confidence score validation
    # This is a simplified example. A real implementation would check
    # confidence scores from the raw_data field if the extraction
    # service provides them.
    # For example:
    # if 'confidence' in expense.raw_data.get('total_field', {}) and \
    #    expense.raw_data['total_field']['confidence'] < 0.9:
    #        raise ValidationError("Total amount has low confidence score.")

    if not expense.line_items:
        # Depending on the use case, line items might not be strictly required.
        # For this example, we'll allow expenses without line items.
        pass

    return True
