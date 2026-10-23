from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

@dataclass
class Invoice:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_total: Optional[float] = None
    line_items: List[LineItem] = None
    currency: Optional[str] = None
    invoice_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    vendor_address: Optional[str] = None
    purchase_order: Optional[str] = None
    due_date: Optional[str] = None
    tax_amount: Optional[float] = None
    service_start_date: Optional[str] = None
    service_end_date: Optional[str] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    payment_terms: Optional[str] = None
    vat_number: Optional[str] = None
    vendor_tax_id: Optional[str] = None
    customer_tax_id: Optional[str] = None
    bank_account_number: Optional[str] = None
    swift_code: Optional[str] = None
    iban_number: Optional[str] = None
    notes: Optional[str] = None
    memo: Optional[str] = None

@dataclass
class Receipt:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    transaction_time: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = None
    currency: Optional[str] = None
    merchant_address: Optional[str] = None
    merchant_phone: Optional[str] = None
    merchant_website: Optional[str] = None
    tip_amount: Optional[float] = None
    payment_method: Optional[str] = None
    card_type: Optional[str] = None
    card_number_last_four_digits: Optional[str] = None
    cashback_amount: Optional[float] = None
    notes: Optional[str] = None

@dataclass
class NormalizedExpense:
    transaction_id: Optional[str] = None
    document_type: Optional[str] = None # 'invoice' or 'receipt'
    transaction_date: Optional[str] = None
    vendor_merchant_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    line_items: List[LineItem] = None
    raw_document_data: Dict[str, Any] = None
    validation_status: Optional[str] = None
    validation_details: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    memo: Optional[str] = None
