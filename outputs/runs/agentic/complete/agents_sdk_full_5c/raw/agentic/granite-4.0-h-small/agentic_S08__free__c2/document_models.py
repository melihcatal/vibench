# [HELPER] document_models.py
"""
Define local request, response, and normalization helpers for Structured Document Extraction.
"""
from __future__ import annotations
import json
from typing import TypedDict, List, Optional

class InvoiceExtractionRequest(TypedDict):
    path: str

class InvoiceExtractionResponse(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: List[dict]

class ReceiptExtractionRequest(TypedDict):
    path: str

class ReceiptExtractionResponse(TypedDict):
    merchant: str
    tax: float
    total: float
    items: List[dict]

class NormalizedExpense(TypedDict):
    vendor: str
    date: str
    amount: float
    line_items: List[dict]

class ValidationRequest(TypedDict):
    vendor: dict
    date: dict
    total: dict
    confidence_threshold: Optional[float] = 0.8

class ValidationResponse(TypedDict):
    valid: bool
    details: str

class ExpenseRecord(TypedDict):
    vendor: str
    date: str
    amount: float
    line_items: List[dict]
