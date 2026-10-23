import boto3
import os
from document_models import DocumentExtractionRequest, DocumentExtractionResponse, ExtractedDocumentFields, LineItem

class DocumentClient:
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.textract_client = boto3.client("textract", region_name=self.region_name)

    def analyze_expense(self, request: DocumentExtractionRequest) -> DocumentExtractionResponse:
        response = self.textract_client.analyze_expense(Document={"Bytes": request.document_bytes})
        
        extracted_documents = []
        for document in response["ExpenseDocuments"]:
            fields = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in document["SummaryFields"]}
            
            line_items = []
            for group in document.get("LineItemGroups", []):
                for item in group["LineItems"]:
                    values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item["LineItemExpenseFields"]}
                    line_items.append(LineItem(
                        description=values.get("ITEM"),
                        quantity=values.get("QUANTITY"),
                        amount=values.get("PRICE")
                    ))
            
            extracted_documents.append(ExtractedDocumentFields(
                vendor=fields.get("VENDOR_NAME"),
                merchant=fields.get("MERCHANT_NAME"), # Textract might also provide merchant name
                date=fields.get("INVOICE_RECEIPT_DATE"),
                total=fields.get("TOTAL"),
                tax=fields.get("TAX"),
                line_items=line_items,
                items=line_items # For receipts, line_items can be used as items
            ))
        
        # Textract returns a single list of ExpenseDocuments, we can assume they are either invoices or receipts
        # For simplicity, I'll put them all into 'invoices' for now, and 'extract_receipt_fields' will handle its specific fields.
        return DocumentExtractionResponse(invoices=extracted_documents)
