from document_models import InvoiceExtraction, NormalizedExpense, ReceiptExtraction


def normalize_invoice_to_expense(
    invoice: InvoiceExtraction, source_document_id: str = ""
) -> NormalizedExpense:
    line_items = []
    for item in invoice.line_items:
        line_items.append(
            {
                "description": item.description.value,
                "quantity": item.quantity.value,
                "unit_price": item.unit_price.value,
                "total_price": item.total_price.value,
                "confidence": min(
                    item.description.confidence,
                    item.quantity.confidence,
                    item.unit_price.confidence,
                    item.total_price.confidence,
                ),
            }
        )
    confidences = [
        invoice.vendor_name.confidence,
        invoice.invoice_date.confidence,
        invoice.invoice_total.confidence,
    ]
    avg_confidence = sum(c for c in confidences if c > 0) / max(
        len([c for c in confidences if c > 0]), 1
    )
    return NormalizedExpense(
        document_type="invoice",
        vendor_or_merchant=invoice.vendor_name.value,
        document_date=invoice.invoice_date.value,
        subtotal=0.0,
        tax=0.0,
        total=float(invoice.invoice_total.value),
        line_items=line_items,
        currency="USD",
        source_document_id=source_document_id,
        extraction_confidence=avg_confidence,
    )


def normalize_receipt_to_expense(
    receipt: ReceiptExtraction, source_document_id: str = ""
) -> NormalizedExpense:
    line_items = []
    for item in receipt.items:
        line_items.append(
            {
                "description": item.description.value,
                "quantity": 1,
                "unit_price": item.price.value,
                "total_price": item.price.value,
                "confidence": item.description.confidence,
            }
        )
    confidences = [
        receipt.merchant_name.confidence,
        receipt.tax_amount.confidence,
        receipt.receipt_total.confidence,
    ]
    avg_confidence = sum(c for c in confidences if c > 0) / max(
        len([c for c in confidences if c > 0]), 1
    )
    return NormalizedExpense(
        document_type="receipt",
        vendor_or_merchant=receipt.merchant_name.value,
        document_date="",
        subtotal=float(receipt.receipt_total.value) - float(receipt.tax_amount.value),
        tax=float(receipt.tax_amount.value),
        total=float(receipt.receipt_total.value),
        line_items=line_items,
        currency="USD",
        source_document_id=source_document_id,
        extraction_confidence=avg_confidence,
    )


def normalize_expense(extraction, source_document_id: str = "") -> NormalizedExpense:
    if isinstance(extraction, InvoiceExtraction):
        return normalize_invoice_to_expense(extraction, source_document_id)
    elif isinstance(extraction, ReceiptExtraction):
        return normalize_receipt_to_expense(extraction, source_document_id)
    else:
        raise TypeError(f"Unsupported extraction type: {type(extraction)}")


def normalize_expense_batch(
    extractions: list, source_document_ids: list[str] = None
) -> list[NormalizedExpense]:
    if source_document_ids is None:
        source_document_ids = [f"doc_{i}" for i in range(len(extractions))]
    results = []
    for extraction, doc_id in zip(extractions, source_document_ids):
        results.append(normalize_expense(extraction, source_document_id=doc_id))
    return results
