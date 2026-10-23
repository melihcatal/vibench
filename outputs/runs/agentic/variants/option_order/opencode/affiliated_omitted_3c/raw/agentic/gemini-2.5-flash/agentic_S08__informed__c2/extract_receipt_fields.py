from document_client import get_document_intelligence_client
from document_models import ExtractedReceipt, LineItem
from azure.ai.documentintelligence.models import AnalyzeResult


def extract_receipt_fields(document_url: str) -> ExtractedReceipt:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document_from_url("prebuilt-receipt", document_url)
    result: AnalyzeResult = poller.result()

    receipt_fields = ExtractedReceipt()
    if result.documents and result.documents[0].fields:
        doc_fields = result.documents[0].fields

        receipt_fields.merchant_name = (
            doc_fields.get("MerchantName") and doc_fields["MerchantName"].value_string
        )
        receipt_fields.transaction_date = (
            doc_fields.get("TransactionDate")
            and doc_fields["TransactionDate"].value_date.isoformat()
            if doc_fields["TransactionDate"].value_date
            else None
        )
        receipt_fields.total_amount = (
            doc_fields.get("Total")
            and doc_fields["Total"].value_currency
            and doc_fields["Total"].value_currency.amount
        )
        receipt_fields.tax_amount = (
            doc_fields.get("TotalTax")
            and doc_fields["TotalTax"].value_currency
            and doc_fields["TotalTax"].value_currency.amount
        )
        receipt_fields.currency = (
            doc_fields.get("Total")
            and doc_fields["Total"].value_currency
            and doc_fields["Total"].value_currency.currency_symbol
        )

        if doc_fields.get("Items") and doc_fields["Items"].value_array:
            for item_field in doc_fields["Items"].value_array:
                if item_field.value_object:
                    item = item_field.value_object
                    receipt_fields.line_items.append(
                        LineItem(
                            description=item.get("Description")
                            and item["Description"].value_string,
                            quantity=item.get("Quantity")
                            and item["Quantity"].value_number,
                            unit_price=item.get("UnitPrice")
                            and item["UnitPrice"].value_currency
                            and item["UnitPrice"].value_currency.amount,
                            total_price=item.get("TotalPrice")
                            and item["TotalPrice"].value_currency
                            and item["TotalPrice"].value_currency.amount,
                        )
                    )
    return receipt_fields
