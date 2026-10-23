import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import DocumentClient
from document_models import DocumentExtractionRequest, ExtractedReceiptFields, LineItem

# Google Cloud Document AI Receipt Parser Processor ID
RECEIPT_PROCESSOR_ID = os.getenv("DOCUMENT_AI_RECEIPT_PROCESSOR_ID")


class ReceiptExtractor:
    def __init__(self):
        if not RECEIPT_PROCESSOR_ID:
            raise ValueError(
                "DOCUMENT_AI_RECEIPT_PROCESSOR_ID environment variable not set."
            )
        self.doc_client = DocumentClient()
        self.processor_path = self.doc_client.get_documentai_processor_path(
            RECEIPT_PROCESSOR_ID
        )

    def extract_fields(
        self, request: DocumentExtractionRequest
    ) -> ExtractedReceiptFields:
        raw_document = documentai.RawDocument(
            content=request.document_content, mime_type=request.mime_type
        )
        process_request = documentai.ProcessRequest(
            name=self.processor_path, raw_document=raw_document
        )

        # Use Document AI to process the document
        result = self.doc_client.documentai_client.process_document(
            request=process_request
        )
        document = result.document

        merchant_name = None
        transaction_date = None
        tax_amount = None
        total_amount = None
        currency = None
        line_items = []

        for entity in document.entities:
            if entity.type == "merchant_name":
                merchant_name = entity.mention_text
            elif entity.type == "transaction_date":
                transaction_date = entity.mention_text
            elif entity.type == "total_amount":
                total_amount = (
                    entity.normalized_value.float_value
                    if entity.normalized_value.HasField("float_value")
                    else None
                )
                currency = entity.normalized_value.currency_code
            elif entity.type == "tax_amount":
                tax_amount = (
                    entity.normalized_value.float_value
                    if entity.normalized_value.HasField("float_value")
                    else None
                )
            elif entity.type == "line_item":
                description = None
                quantity = None
                unit_price = None
                total_price = None
                for sub_entity in entity.properties:
                    if sub_entity.type == "description":
                        description = sub_entity.mention_text
                    elif sub_entity.type == "quantity":
                        quantity = (
                            sub_entity.normalized_value.float_value
                            if sub_entity.normalized_value.HasField("float_value")
                            else None
                        )
                    elif sub_entity.type == "unit_price":
                        unit_price = (
                            sub_entity.normalized_value.float_value
                            if sub_entity.normalized_value.HasField("float_value")
                            else None
                        )
                    elif (
                        sub_entity.type == "amount"
                    ):  # Document AI often uses 'amount' for line item total
                        total_price = (
                            sub_entity.normalized_value.float_value
                            if sub_entity.normalized_value.HasField("float_value")
                            else None
                        )
                line_items.append(
                    LineItem(
                        description=description,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                    )
                )

        return ExtractedReceiptFields(
            merchant_name=merchant_name,
            transaction_date=transaction_date,
            tax_amount=tax_amount,
            total_amount=total_amount,
            currency=currency,
            line_items=line_items,
            raw_text=document.text,
        )
