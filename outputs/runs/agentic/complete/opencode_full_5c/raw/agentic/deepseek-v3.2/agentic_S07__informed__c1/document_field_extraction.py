import os
import json
from typing import Dict, Any, Optional, List
from document_client import DocumentClient
from document_models import FieldExtractionResult

def extract_invoice_fields(image_path: str, region: Optional[str] = None) -> FieldExtractionResult:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()
    
    image_bytes = client.read_image_bytes(image_path)
    
    response = textract_client.analyze_expense(
        Document={"Bytes": image_bytes}
    )
    
    return parse_expense_response(response)

def parse_expense_response(response: Dict[str, Any]) -> FieldExtractionResult:
    expense_documents = response.get("ExpenseDocuments", [])
    if not expense_documents:
        return FieldExtractionResult(
            fields={},
            confidence_scores={},
            document_type="unknown"
        )
    
    expense_doc = expense_documents[]
    summary_fields = expense_doc.get("SummaryFields", [])
    
    fields = {}
    confidence_scores = {}
    
    for field in summary_fields:
        field_type = field.get("Type", {}).get("Text", "")
        if not field_type:
            continue
        
        value_text = ""
        value_confidence = 0.0
        
        value_detection = field.get("ValueDetection", {})
        if value_detection:
            value_text = value_detection.get("Text", "")
            value_confidence = value_detection.get("Confidence", 0.0)
        
        if value_text:
            fields[field_type] = value_text
            confidence_scores[field_type] = value_confidence
    
    document_type = "invoice"
    
    return FieldExtractionResult(
        fields=fields,
        confidence_scores=confidence_scores,
        document_type=document_type
    )

def extract_receipt_fields(image_path: str, region: Optional[str] = None) -> FieldExtractionResult:
    result = extract_invoice_fields(image_path, region)
    
    receipt_fields = {}
    receipt_confidences = {}
    
    receipt_field_mapping = {
        "VENDOR_NAME": "vendor",
        "RECEIVER_NAME": "receiver",
        "TOTAL": "total",
        "INVOICE_RECEIPT_DATE": "date",
        "INVOICE_RECEIPT_ID": "receipt_id",
        "SUBTOTAL": "subtotal",
        "TAX": "tax",
        "DUE_DATE": "due_date"
    }
    
    for field_type, value in result.fields.items():
        if field_type in receipt_field_mapping:
            mapped_name = receipt_field_mapping[field_type]
            receipt_fields[mapped_name] = value
            if field_type in result.confidence_scores:
                receipt_confidences[mapped_name] = result.confidence_scores[field_type]
    
    return FieldExtractionResult(
        fields=receipt_fields,
        confidence_scores=receipt_confidences,
        document_type="receipt"
    )

def extract_specific_fields(image_path: str, field_names: List[str], region: Optional[str] = None) -> Dict[str, Any]:
    result = extract_invoice_fields(image_path, region)
    
    extracted = {}
    for field_name in field_names:
        for field_type, value in result.fields.items():
            if field_name.lower() in field_type.lower():
                extracted[field_name] = {
                    "value": value,
                    "confidence": result.confidence_scores.get(field_type, 0.0),
                    "original_field": field_type
                }
                break
        if field_name not in extracted:
            extracted[field_name] = {
                "value": "",
                "confidence": 0.0,
                "original_field": ""
            }
    
    return extracted

def extract_line_items(image_path: str, region: Optional[str] = None) -> List[Dict[str, Any]]:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()
    
    image_bytes = client.read_image_bytes(image_path)
    
    response = textract_client.analyze_expense(
        Document={"Bytes": image_bytes}
    )
    
    line_items = []
    expense_documents = response.get("ExpenseDocuments", [])
    
    for expense_doc in expense_documents:
        for line_item_group in expense_doc.get("LineItemGroups", []):
            for line_item in line_item_group.get("LineItems", []):
                item_fields = {}
                for field in line_item.get("LineItemExpenseFields", []):
                    field_type = field.get("Type", {}).get("Text", "")
                    value_detection = field.get("ValueDetection", {})
                    if field_type and value_detection:
                        item_fields[field_type] = {
                            "value": value_detection.get("Text", ""),
                            "confidence": value_detection.get("Confidence", 0.0)
                        }
                
                if item_fields:
                    line_items.append(item_fields)
    
    return line_items

def validate_extracted_fields(field_extraction_result: FieldExtractionResult, required_fields: List[str]) -> Dict[str, bool]:
    validation = {}
    
    for field in required_fields:
        field_found = False
        for extracted_field in field_extraction_result.fields.keys():
            if field.lower() in extracted_field.lower():
                field_found = True
                break
        
        validation[field] = field_found
    
    return validation