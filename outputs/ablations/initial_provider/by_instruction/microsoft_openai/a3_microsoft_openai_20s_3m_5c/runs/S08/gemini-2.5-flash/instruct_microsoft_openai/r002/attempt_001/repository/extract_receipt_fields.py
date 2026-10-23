from document_client import DocumentClients
from document_models import Receipt, LineItem
from azure.ai.documentintelligence.models import ContentFormat
from typing import BinaryIO

def extract_receipt_fields(receipt_document: BinaryIO) -> Receipt:
    clients = DocumentClients()
    if not clients.document_intelligence_client:
        raise ValueError("Azure Document Intelligence client not initialized.")

    poller = clients.document_intelligence_client.begin_analyze_document(
        "prebuilt-receipt", receipt_document, content_type="application/pdf"
    )
    result = poller.result()

    receipt_fields = Receipt(line_items=[])

    if result.documents:
        for doc in result.documents:
            if doc.doc_type == "prebuilt-receipt":
                receipt_fields.merchant_name = doc.fields.get("MerchantName") and doc.fields["MerchantName"].content
                receipt_fields.transaction_date = doc.fields.get("TransactionDate") and doc.fields["TransactionDate"].content
                receipt_fields.transaction_time = doc.fields.get("TransactionTime") and doc.fields["TransactionTime"].content
                receipt_fields.total_amount = doc.fields.get("Total") and doc.fields["Total"].value
                receipt_fields.tax_amount = doc.fields.get("TotalTax") and doc.fields["TotalTax"].value
                receipt_fields.currency = doc.fields.get("Currency") and doc.fields["Currency"].content
                receipt_fields.merchant_address = doc.fields.get("MerchantAddress") and doc.fields["MerchantAddress"].content
                receipt_fields.merchant_phone = doc.fields.get("MerchantPhoneNumber") and doc.fields["MerchantPhoneNumber"].content
                receipt_fields.merchant_website = doc.fields.get("Website") and doc.fields["Website"].content
                receipt_fields.tip_amount = doc.fields.get("Tip") and doc.fields["Tip"].value
                receipt_fields.payment_method = doc.fields.get("PaymentMethod") and doc.fields["PaymentMethod"].content
                receipt_fields.card_type = doc.fields.get("CardType") and doc.fields["CardType"].content
                receipt_fields.card_number_last_four_digits = doc.fields.get("CardNumber") and doc.fields["CardNumber"].content
                receipt_fields.cashback_amount = doc.fields.get("Cashback") and doc.fields["Cashback"].value
                receipt_fields.notes = doc.fields.get("Notes") and doc.fields["Notes"].content

                if "Items" in doc.fields:
                    for item_field in doc.fields["Items"].value:
                        line_item = LineItem(
                            description=item_field.get("Description") and item_field["Description"].content,
                            quantity=item_field.get("Quantity") and item_field["Quantity"].value,
                            unit_price=item_field.get("UnitPrice") and item_field["UnitPrice"].value,
                            total_price=item_field.get("TotalPrice") and item_field["TotalPrice"].value,
                        )
                        receipt_fields.line_items.append(line_item)
    return receipt_fields
