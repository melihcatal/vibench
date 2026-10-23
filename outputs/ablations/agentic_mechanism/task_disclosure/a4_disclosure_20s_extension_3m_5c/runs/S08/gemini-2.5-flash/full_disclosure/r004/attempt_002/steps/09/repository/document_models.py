
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class DocumentExtractionRequest(BaseModel):
    document_url: str = Field(..., description="URL of the document to be processed.")
    document_type: str = Field(..., description="Type of the document (e.g., 'invoice', 'receipt').")
    
class ExtractedField(BaseModel):
    field_name: str
    field_value: Any
    confidence: float

class DocumentExtractionResponse(BaseModel):
    document_id: str
    extracted_fields: List[ExtractedField]
    raw_response: Dict[str, Any]

class NormalizedExpense(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: Optional[List[Dict[str, Any]]] = None
    
class DocumentNormalizationHelper:
    @staticmethod
    def normalize_extracted_data(extracted_data: DocumentExtractionResponse) -> NormalizedExpense:
        normalized_expense = NormalizedExpense()
        
        for field in extracted_data.extracted_fields:
            if field.field_name == "merchant_name":
                normalized_expense.merchant_name = field.field_value
            elif field.field_name == "transaction_date":
                normalized_expense.transaction_date = field.field_value
            elif field.field_name == "total_amount":
                normalized_expense.total_amount = float(field.field_value)
            elif field.field_name == "currency":
                normalized_expense.currency = field.field_value
            elif field.field_name == "line_items":
                normalized_expense.line_items = field.field_value
                
        return normalized_expense
