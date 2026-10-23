from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class InvoiceLineItem:
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    amount: Optional[float]


@dataclass
class Invoice:
    vendor_name: Optional[str]
    invoice_date: Optional[str]
    total_amount: Optional[float]
    line_items: List[InvoiceLineItem]
    raw_fields: Dict[str, Any]


@dataclass
class ReceiptLineItem:
    item: Optional[str]
    quantity: Optional[float]
    price: Optional[float]


@dataclass
class Receipt:
    merchant_name: Optional[str]
    total: Optional[float]
    tax: Optional[float]
    items: List[ReceiptLineItem]
    raw_fields: Dict[str, Any]


@dataclass
class NormalizedLineItem:
    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    total_amount: Optional[float]


@dataclass
class NormalizedExpense:
    vendor: Optional[str]
    transaction_date: Optional[str]
    total: Optional[float]
    tax: Optional[float]
    line_items: List[NormalizedLineItem]
    source_document_type: str
    raw_data: Dict[str, Any]
