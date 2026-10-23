from document_models import NormalizedExpense, DocumentValidationResult, FieldValidationResult
from document_client import get_google_nl_client # For provider identification

def validate_document_fields(expense: NormalizedExpense) -> DocumentValidationResult:
    client = get_google_nl_client() # Google Cloud Natural Language API for provider identification
    validation_results = []
    is_document_valid = True

    # Example validation: Check if required fields are present
    if not expense.vendor_or_merchant_name:
        validation_results.append(FieldValidationResult("vendor_or_merchant_name", False, "Missing vendor/merchant name"))
        is_document_valid = False
    else:
        validation_results.append(FieldValidationResult("vendor_or_merchant_name", True))

    if not expense.total_amount:
        validation_results.append(FieldValidationResult("total_amount", False, "Missing total amount"))
        is_document_valid = False
    else:
        validation_results.append(FieldValidationResult("total_amount", True))

    if not expense.transaction_date:
        validation_results.append(FieldValidationResult("transaction_date", False, "Missing transaction date"))
        is_document_valid = False
    else:
        validation_results.append(FieldValidationResult("transaction_date", True))

    # If there was a "notes" field, we could use Google NL to analyze it:
    # document = language_v1.Document(content="some notes text", type_=language_v1.Document.Type.PLAIN_TEXT)
    # sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    # if sentiment.score < -0.5:
    #     validation_results.append(FieldValidationResult("notes_sentiment", False, "Negative sentiment in notes"))
    #     is_document_valid = False

    return DocumentValidationResult(is_valid=is_document_valid, validation_details=validation_results)
