# [SAME-SCENARIO] validate_document_fields.py
from pydantic import BaseModel, Field, ValidationError, validator
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse

class InvoiceValidationResponse(BaseModel):
    vendor: str = Field(..., description='Name of the vendor')
    date: str = Field(..., description='Invoice date')
    total: str = Field(..., description='Total amount as string')
    line_items: list[dict] = Field(default_factory=list, description='List of line-item dicts')

class ReceiptValidationResponse(BaseModel):
    merchant: str = Field(..., description='Merchant name')
    tax: str = Field(..., description='Tax amount')
    total: str = Field(..., description='Total amount as string')
    items: list[dict] = Field(default_factory=list, description='List of item dicts')

def validate_document_fields(extracted) -> bool:
    """Validate that required structured fields and confidence scores are present in the extraction result.

    Returns True if validation succeeds, otherwise raises ValidationError.
    """
    if isinstance(extracted, InvoiceExtractionResponse):
        model = InvoiceValidationResponse.from_orm(extracted)
    elif isinstance(extracted, ReceiptExtractionResponse):
        model = ReceiptValidationResponse.from_orm(extracted)
    else:
        raise TypeError('Unsupported extraction type')
    # Pydantic will raise if any required fields are missing or type invalid
    model.validate()
    return True