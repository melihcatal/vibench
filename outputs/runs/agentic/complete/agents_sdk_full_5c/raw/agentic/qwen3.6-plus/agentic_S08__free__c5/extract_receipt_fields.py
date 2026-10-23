"""
Extract merchant, tax, total, and items from a receipt using Azure AI Document Intelligence.
Provider: Azure AI Document Intelligence (formerly Form Recognizer) - Receipt model
"""

import os
from typing import Optional, List, Dict, Any
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from document_models import ReceiptExtractionRequest, ReceiptExtractionResponse, ReceiptItem


def extract_receipt_fields(
    document_path: Optional[str] = None,
    document_bytes: Optional[bytes] = None,
    azure_endpoint: Optional[str] = None,
    azure_api_key: Optional[str] = None,
    model_id: str = "prebuilt-receipt",
) -> ReceiptExtractionResponse:
    """
    Extract structured receipt fields using Azure Document Intelligence Receipt model.
    
    Uses the prebuilt-receipt model (prebuilt-receipt) which extracts:
    - Merchant name
    - Transaction date
    - Total amount
    - Tax amount
    - Individual line items
    
    Args:
        document_path: Path to receipt PDF/image file
        document_bytes: Raw bytes of receipt document
        azure_endpoint: Azure Document Intelligence endpoint URL
        azure_api_key: Azure API key
        model_id: Azure model ID (default: prebuilt-receipt)
    
    Returns:
        ReceiptExtractionResponse with extracted fields
    """
    endpoint = azure_endpoint or os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "https://default-resource.cognitiveservices.azure.com/",
    )
    api_key = azure_api_key or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_API_KEY", "")
    
    if not api_key:
        raise ValueError("Azure API key must be provided via parameter or AZURE_DOCUMENT_INTELLIGENCE_API_KEY env var")
    
    client = DocumentAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )
    
    if document_bytes:
        poller = client.begin_analyze_document(model_id, document=document_bytes)
    elif document_path:
        with open(document_path, "rb") as f:
            poller = client.begin_analyze_document(model_id, document=f)
    else:
        raise ValueError("Either document_path or document_bytes must be provided")
    
    result = poller.result()
    return _parse_azure_receipt_result(result)


def _parse_azure_receipt_result(result: Any) -> ReceiptExtractionResponse:
    """Parse Azure Document Intelligence receipt result into ReceiptExtractionResponse."""
    merchant = None
    merchant_confidence = 0.0
    transaction_date = None
    date_confidence = 0.0
    total_amount = None
    total_confidence = 0.0
    tax_amount = None
    tax_confidence = 0.0
    subtotal_amount = None
    items: List[ReceiptItem] = []
    
    for doc in result.documents:
        fields = doc.fields
        
        merchant_field = fields.get("MerchantName")
        if merchant_field:
            merchant = merchant_field.value
            merchant_confidence = merchant_field.confidence or 0.0
        
        date_field = fields.get("TransactionDate")
        if date_field:
            transaction_date = str(date_field.value)
            date_confidence = date_field.confidence or 0.0
        
        total_field = fields.get("Total")
        if total_field:
            total_amount = total_field.value
            total_confidence = total_field.confidence or 0.0
        
        tax_field = fields.get("TotalTax")
        if tax_field:
            tax_amount = tax_field.value
            tax_confidence = tax_field.confidence or 0.0
        
        subtotal_field = fields.get("Subtotal")
        if subtotal_field:
            subtotal_amount = subtotal_field.value
        
        items_field = fields.get("Items")
        if items_field and items_field.value:
            for item_entry in items_field.value:
                item_data: Dict[str, Any] = {}
                if isinstance(item_entry, dict):
                    for key, field in item_entry.items():
                        item_data[key] = field.value if hasattr(field, "value") else field
                
                description = item_data.get("Description")
                total_price = item_data.get("TotalPrice")
                quantity = item_data.get("Quantity")
                unit_price = item_data.get("UnitPrice")
                confidence = item_data.get("Confidence", 0.0)
                
                items.append(
                    ReceiptItem(
                        description=str(description) if description else None,
                        total_price=float(total_price) if total_price is not None else None,
                        quantity=float(quantity) if quantity is not None else None,
                        unit_price=float(unit_price) if unit_price is not None else None,
                        confidence=confidence if isinstance(confidence, float) else 0.0,
                    )
                )
    
    return ReceiptExtractionResponse(
        merchant=merchant,
        transaction_date=transaction_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        subtotal_amount=subtotal_amount,
        items=items,
        merchant_confidence=merchant_confidence,
        date_confidence=date_confidence,
        total_confidence=total_confidence,
        tax_confidence=tax_confidence,
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_receipt_fields.py <receipt_file_path>")
        sys.exit(1)
    
    result = extract_receipt_fields(document_path=sys.argv[1])
    print(result.model_dump_json(indent=2))
