from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpense,
    LineItem,
)


def normalize_expense(
    extraction_result: [InvoiceExtractionResult, ReceiptExtractionResult],
    document_type: str,
) -> NormalizedExpense:
    if document_type == "invoice":
        if not isinstance(extraction_result, InvoiceExtractionResult):
            raise ValueError(
                "Expected InvoiceExtractionResult for invoice document type."
            )
        return NormalizedExpense(
            document_type="invoice",
            vendor_merchant_name=extraction_result.vendor_name,
            transaction_date=extraction_result.invoice_date,
            total_amount=extraction_result.total_amount,
            currency=extraction_result.currency,
            tax_amount=None,  # Invoice parser might not always provide tax directly
            line_items=extraction_result.line_items,
            confidence_scores={},
        )
    elif document_type == "receipt":
        if not isinstance(extraction_result, ReceiptExtractionResult):
            raise ValueError(
                "Expected ReceiptExtractionResult for receipt document type."
            )
        return NormalizedExpense(
            document_type="receipt",
            vendor_merchant_name=extraction_result.merchant_name,
            transaction_date=extraction_result.transaction_date,
            total_amount=extraction_result.total_amount,
            currency=extraction_result.currency,
            tax_amount=extraction_result.tax_amount,
            line_items=extraction_result.line_items,
            confidence_scores={},
        )
    else:
        raise ValueError(f"Unsupported document type: {document_type}")
