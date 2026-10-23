# provider: Microsoft Form Recognizer (Azure) - validation through schema enforcement

from azure.core.exceptions import HttpResponseError
from pydantic import BaseModel, ValidationError, Field, validator
from document_models import InvoiceFieldsResponse, ReceiptFieldsResponse

# Local helper import for configuration
from document_client import get_azure_api_version

API_VERSION = get_azure_api_version()


class InvoiceSchema(BaseModel):
    vendor: str = Field(..., description="Payee name")
    date: str = Field(
        ..., pattern=r"\\d{4}-\\d{2}-\\d{2}", description="YYYY-MM-DD invoice date"
    )
    total: str = Field(
        ...,
        regex=r"\\d+(?:\.\\d{2})?",
        description="Numeric total with optional two decimal places",
    )
    line_items: list[dict] = Field(
        ...,
        description="Ordered list of dicts with keys: description, quantity, unit_price, total",
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Overall confidence of extraction"
    )


class ReceiptSchema(BaseModel):
    merchant: str = Field(..., min_length=1, description="Merchant name on receipt")
    tax: str = Field(..., regex=r"\\d+(?:\.\\d{2})?", description="Numeric tax amount")
    total: str = Field(
        ..., regex=r"\\d+(?:\.\\d{2})?", description="Numeric total amount"
    )
    items: list[str] = Field(
        ..., min_items=1, description="List of line item descriptions"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Overall confidence of extraction"
    )


def validate_invoice_fields(response: InvoiceFieldsResponse) -> InvoiceFieldsResponse:
    try:
        validated = InvoiceSchema(**response.dict())
        # attach pydantic validated data back to original response object or return new one
        return InvoiceFieldsResponse(
            vendor=validated.vendor,
            date=validated.date,
            total=validated.total,
            line_items=validated.line_items,
            confidence=validated.confidence,
        )
    except ValidationError as e:
        raise HttpResponseError(
            status_code=400,
            message=f"Invalid invoice fields: {e.json()}",
        )


def validate_receipt_fields(response: ReceiptFieldsResponse) -> ReceiptFieldsResponse:
    try:
        validated = ReceiptSchema(**response.dict())
        return ReceiptFieldsResponse(
            merchant=validated.merchant,
            tax=validated.tax,
            total=validated.total,
            items=validated.items,
            confidence=validated.confidence,
        )
    except ValidationError as e:
        raise HttpResponseError(
            status_code=400,
            message=f"Invalid receipt fields: {e.json()}",
        )


if __name__ == "__main__":
    from pprint import pprint
    import json

    # Example usage - validate a sample extracted JSON payload
    sample = {
        "vendor": "Acme Corp",
        "date": "2024-06-15",
        "total": "123.45",
        "line_items": [
            {
                "description": "Item A",
                "quantity": "2",
                "unit_price": "10.00",
                "total": "20.00",
            },
            {
                "description": "Item B",
                "quantity": "1",
                "unit_price": "15.00",
                "total": "15.00",
            },
        ],
        "confidence": 0.95,
    }
    validated = validate_invoice_fields(InvoiceFieldsResponse(**sample))
    pprint(validated.dict())
