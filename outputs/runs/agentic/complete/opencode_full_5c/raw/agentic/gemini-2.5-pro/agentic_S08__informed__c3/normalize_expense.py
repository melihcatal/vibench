from document_models import Invoice, Receipt, NormalizedExpense, NormalizedLineItem


def normalize_from_invoice(invoice: Invoice) -> NormalizedExpense:
    line_items = [
        NormalizedLineItem(
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_amount=item.amount,
        )
        for item in invoice.line_items
    ]
    return NormalizedExpense(
        vendor=invoice.vendor_name,
        transaction_date=invoice.invoice_date,
        total=invoice.total_amount,
        tax=None,  # Invoices might not always have a separate tax field
        line_items=line_items,
        source_document_type="invoice",
        raw_data=invoice.raw_fields,
    )


def normalize_from_receipt(receipt: Receipt) -> NormalizedExpense:
    line_items = [
        NormalizedLineItem(
            description=item.item,
            quantity=item.quantity,
            unit_price=item.price,  # Assuming price is per unit
            total_amount=item.price,
        )
        for item in receipt.items
    ]
    return NormalizedExpense(
        vendor=receipt.merchant_name,
        transaction_date=None,  # Receipts may not have an explicit date field
        total=receipt.total,
        tax=receipt.tax,
        line_items=line_items,
        source_document_type="receipt",
        raw_data=receipt.raw_fields,
    )
