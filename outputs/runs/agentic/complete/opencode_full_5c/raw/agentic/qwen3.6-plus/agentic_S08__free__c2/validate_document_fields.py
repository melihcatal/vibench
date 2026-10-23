from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_models import (
    InvoiceFields,
    ReceiptFields,
    FieldValidationResult,
    DocumentValidationResult,
    REQUIRED_INVOICE_FIELDS,
    REQUIRED_RECEIPT_FIELDS,
    REQUIRED_EXPENSE_FIELDS,
    MINIMUM_CONFIDENCE_THRESHOLD,
)
from document_client import (
    AZURE_ENDPOINT,
    AZURE_API_KEY,
    validate_azure_credentials,
    parse_azure_document_intelligence_response,
)


def validate_document_fields_invoice(
    invoice: InvoiceFields,
    required_fields: list[str] | None = None,
    min_confidence: float = MINIMUM_CONFIDENCE_THRESHOLD,
) -> DocumentValidationResult:
    fields_to_check = required_fields or REQUIRED_INVOICE_FIELDS
    field_results = []

    for field_name in fields_to_check:
        result = _validate_single_field(invoice, field_name, min_confidence)
        field_results.append(result)

    overall_valid = all(r.valid for r in field_results)
    overall_confidence = invoice.confidence

    return DocumentValidationResult(
        document_type="invoice",
        overall_valid=overall_valid,
        field_results=field_results,
        overall_confidence=overall_confidence,
        validation_timestamp="",
    )


def validate_document_fields_receipt(
    receipt: ReceiptFields,
    required_fields: list[str] | None = None,
    min_confidence: float = MINIMUM_CONFIDENCE_THRESHOLD,
) -> DocumentValidationResult:
    fields_to_check = required_fields or REQUIRED_RECEIPT_FIELDS
    field_results = []

    for field_name in fields_to_check:
        result = _validate_single_field(receipt, field_name, min_confidence)
        field_results.append(result)

    overall_valid = all(r.valid for r in field_results)
    overall_confidence = receipt.confidence

    return DocumentValidationResult(
        document_type="receipt",
        overall_valid=overall_valid,
        field_results=field_results,
        overall_confidence=overall_confidence,
        validation_timestamp="",
    )


def validate_document_fields_with_azure(
    document_bytes: bytes,
    model_id: str = "prebuilt-receipt",
    mime_type: str = "application/pdf",
) -> DocumentValidationResult:
    if not validate_azure_credentials():
        raise ValueError(
            "Azure Document Intelligence credentials not configured. "
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY."
        )

    client = DocumentAnalysisClient(
        endpoint=AZURE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_API_KEY),
    )

    poller = client.begin_analyze_document(
        model_id=model_id,
        document=document_bytes,
        content_type=mime_type,
    )
    result = poller.result()

    parsed = parse_azure_document_intelligence_response(
        type("Response", (), {"content": result})()
    )

    field_results = []
    azure_fields = parsed.get("fields", {})
    for field_name, field_data in azure_fields.items():
        confidence = field_data.get("confidence", 0.0)
        value = field_data.get("value", "")
        present = value is not None and value != ""
        valid = present and confidence >= MINIMUM_CONFIDENCE_THRESHOLD

        issues = []
        if not present:
            issues.append(f"Field '{field_name}' is missing")
        if present and confidence < MINIMUM_CONFIDENCE_THRESHOLD:
            issues.append(
                f"Field '{field_name}' confidence {confidence:.2f} below threshold {MINIMUM_CONFIDENCE_THRESHOLD}"
            )

        field_results.append(
            FieldValidationResult(
                field_name=field_name,
                present=present,
                valid=valid,
                confidence=confidence,
                issues=issues,
            )
        )

    overall_valid = all(r.valid for r in field_results)
    overall_confidence = parsed.get("confidence", 0.0)

    return DocumentValidationResult(
        document_type=model_id,
        overall_valid=overall_valid,
        field_results=field_results,
        overall_confidence=overall_confidence,
        validation_timestamp="",
    )


def _validate_single_field(
    document: InvoiceFields | ReceiptFields,
    field_name: str,
    min_confidence: float,
) -> FieldValidationResult:
    value = getattr(document, field_name, None)
    present = value is not None

    if isinstance(value, list):
        present = len(value) > 0

    valid = present
    issues = []

    if not present:
        valid = False
        issues.append(f"Required field '{field_name}' is missing")
    elif isinstance(value, (int, float)) and value <= 0:
        valid = False
        issues.append(f"Field '{field_name}' has invalid value: {value}")
    elif isinstance(value, str) and not value.strip():
        valid = False
        issues.append(f"Field '{field_name}' is empty")

    if document.confidence < min_confidence:
        issues.append(
            f"Document confidence {document.confidence:.2f} below threshold {min_confidence}"
        )

    return FieldValidationResult(
        field_name=field_name,
        present=present,
        valid=valid,
        confidence=document.confidence,
        issues=issues,
    )


def validate_expense_record_fields(
    expense_record: dict,
    required_fields: list[str] | None = None,
    min_confidence: float = MINIMUM_CONFIDENCE_THRESHOLD,
) -> DocumentValidationResult:
    fields_to_check = required_fields or REQUIRED_EXPENSE_FIELDS
    field_results = []

    for field_name in fields_to_check:
        value = expense_record.get(field_name)
        present = value is not None

        if isinstance(value, list):
            present = len(value) > 0

        valid = present
        issues = []

        if not present:
            valid = False
            issues.append(f"Required field '{field_name}' is missing")
        elif (
            isinstance(value, (int, float))
            and value <= 0
            and field_name == "total_amount"
        ):
            valid = False
            issues.append(f"Field '{field_name}' has invalid value: {value}")

        record_confidence = expense_record.get("confidence", 0.0)
        if record_confidence < min_confidence:
            issues.append(
                f"Record confidence {record_confidence:.2f} below threshold {min_confidence}"
            )

        field_results.append(
            FieldValidationResult(
                field_name=field_name,
                present=present,
                valid=valid,
                confidence=record_confidence,
                issues=issues,
            )
        )

    overall_valid = all(r.valid for r in field_results)
    overall_confidence = expense_record.get("confidence", 0.0)

    return DocumentValidationResult(
        document_type=expense_record.get("document_type", "expense"),
        overall_valid=overall_valid,
        field_results=field_results,
        overall_confidence=overall_confidence,
        validation_timestamp="",
    )
