# Data model definitions for Structured Document Extraction workflow

from __future__ import annotations
from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional
from enum import Enum


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InvoiceField(BaseModel):
    name: str = Field(..., description="Field identifier as used by provider")
    value: Optional[str] = Field(None, description="Extracted raw value")
    confidence: ConfidenceLevel = Field(..., description="Confidence of extraction")


class InvoiceFieldsResponse(BaseModel):
    vendor: Optional[InvoiceField] = Field(None, description="Payee of the invoice")
    date: Optional[InvoiceField] = Field(None, description="Invoice issue/payable date")
    total: Optional[InvoiceField] = Field(None, description="Total amount payable")
    line_items: Optional[List[dict]] = Field(
        None, description="Parsed line-item details"
    )
    overall_confidence: ConfidenceLevel = Field(
        ..., description="Overall extraction confidence"
    )


class ReceiptField(BaseModel):
    name: str = Field(..., description="Field identifier as used by provider")
    value: Optional[str] = Field(None, description="Extracted raw value")
    confidence: ConfidenceLevel = Field(..., description="Confidence of extraction")


class ReceiptFieldsResponse(BaseModel):
    merchant: Optional[ReceiptField] = Field(
        None, description="Merchant name on receipt"
    )
    tax: Optional[ReceiptField] = Field(None, description="Tax amount")
    total: Optional[ReceiptField] = Field(None, description="Total amount")
    items: Optional[List[str]] = Field(
        None, description="List of line item descriptions"
    )
    overall_confidence: ConfidenceLevel = Field(
        ..., description="Overall extraction confidence"
    )


class NormalizedExpense(BaseModel):
    vendor: Optional[str] = Field(None, description="Standardized payee name")
    date: Optional[str] = Field(None, description="ISO or parsed date string")
    total: Optional[str] = Field(None, description="Standardized total amount")
    line_items: Optional[List[dict]] = Field(
        None, description="Normalized line-item dicts"
    )
    confidence: ConfidenceLevel = Field(
        ..., description="Overall confidence after normalization"
    )


class ModerationResult(BaseModel):
    content: Optional[str] = Field(
        None, description="Original vendor note or memo text"
    )
    is_safe: bool = Field(..., description="Boolean flag for safety check")
    reason: Optional[str] = Field(None, description="Reason for flagging as unsafe")


class TranslationResult(BaseModel):
    source_text: str = Field(..., description="Original extracted text")
    target_text: str = Field(..., description="Translated text")
    source_language: str = Field(..., description="ISO 639-1 source language code")
    target_language: str = Field(..., description="ISO 639-1 target language code")


class StoreRecord(BaseModel):
    # Minimal record persisted to a managed document store (e.g., Azure Cosmos DB, GCS JSONL)
    expense_id: str = Field(..., description="Unique identifier for the expense record")
    normalized: NormalizedExpense = Field(..., description="Normalized expense payload")
    moderation: Optional[ModerationResult] = Field(
        None, description="Safety moderation outcome"
    )
    translation: Optional[TranslationResult] = Field(
        None, description="Translation outcome"
    )


if __name__ == "__main__":
    # Simple validation test
    sample_invoice = InvoiceFieldsResponse(
        overall_confidence=ConfidenceLevel.HIGH,
        vendor=InvoiceField(
            name="vendor", value="Acme Corp", confidence=ConfidenceLevel.HIGH
        ),
        date=InvoiceField(
            name="date", value="2024-07-10", confidence=ConfidenceLevel.HIGH
        ),
        total=InvoiceField(
            name="total", value="$123.45", confidence=ConfidenceLevel.HIGH
        ),
        line_items=[
            {
                "description": "Widget",
                "quantity": "2",
                "unit_price": "$50",
                "total": "$100",
            }
        ],
    )
    print("Invoice validation OK:", sample_invoice.json())
