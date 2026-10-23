from typing import Union, Dict, Any

from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpenseRecord,
    normalize_invoice_to_expense,
    normalize_receipt_to_expense,
)


def normalize_expense(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    source_model: str = "",
) -> NormalizedExpenseRecord:
    if isinstance(extraction_result, InvoiceExtractionResult):
        model_id = source_model or "azure-di-prebuilt-invoice"
        return normalize_invoice_to_expense(extraction_result, source_model=model_id)
    elif isinstance(extraction_result, ReceiptExtractionResult):
        model_id = source_model or "azure-di-prebuilt-receipt"
        return normalize_receipt_to_expense(extraction_result, source_model=model_id)
    else:
        raise ValueError(
            f"Unsupported extraction result type: {type(extraction_result)}"
        )


def normalize_expense_to_dict(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    source_model: str = "",
) -> Dict[str, Any]:
    record = normalize_expense(extraction_result, source_model=source_model)
    return record.to_dict()


def batch_normalize_expenses(
    extraction_results: list,
    source_models: list = None,
) -> list:
    normalized = []
    for i, result in enumerate(extraction_results):
        model = source_models[i] if source_models and i < len(source_models) else ""
        normalized.append(normalize_expense(result, source_model=model))
    return normalized
