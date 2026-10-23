from document_models import (
    ExtractedInvoiceFields,
    ExtractedReceiptFields,
    NormalizedExpense,
)


class ExpenseNormalizer:
    def normalize_invoice(
        self, invoice_fields: ExtractedInvoiceFields
    ) -> NormalizedExpense:
        return NormalizedExpense(
            document_type="invoice",
            vendor_name=invoice_fields.vendor_name,
            invoice_date=invoice_fields.invoice_date,
            transaction_date=invoice_fields.invoice_date,  # Map invoice_date to transaction_date for consistency
            total_amount=invoice_fields.total_amount,
            currency=invoice_fields.currency,
            line_items=invoice_fields.line_items,
            raw_document_text=invoice_fields.raw_text,
            confidence_scores={  # Placeholder for confidence scores
                "vendor_name": 0.0,  # Actual confidence would come from Document AI output
                "invoice_date": 0.0,
                "total_amount": 0.0,
            },
        )

    def normalize_receipt(
        self, receipt_fields: ExtractedReceiptFields
    ) -> NormalizedExpense:
        return NormalizedExpense(
            document_type="receipt",
            merchant_name=receipt_fields.merchant_name,
            transaction_date=receipt_fields.transaction_date,
            tax_amount=receipt_fields.tax_amount,
            total_amount=receipt_fields.total_amount,
            currency=receipt_fields.currency,
            line_items=receipt_fields.line_items,
            raw_document_text=receipt_fields.raw_text,
            confidence_scores={  # Placeholder for confidence scores
                "merchant_name": 0.0,
                "transaction_date": 0.0,
                "total_amount": 0.0,
                "tax_amount": 0.0,
            },
        )
