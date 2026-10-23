from typing import Dict, Any, Optional
from datetime import datetime
from document_models import ExpenseSchema, InvoiceSchema, ReceiptSchema

class ExpenseNormalizer:
    def normalize_invoice(self, extracted_data: Dict[str, Any]) -> ExpenseSchema:
        normalized = {
            "source_type": "invoice",
            "vendor": extracted_data.get("vendor", ""),
            "date": self._parse_date(extracted_data.get("date")),
            "total_amount": self._parse_amount(extracted_data.get("total")),
            "line_items": self._normalize_line_items(extracted_data.get("line_items", [])),
            "currency": "USD",
            "confidence": extracted_data.get("confidence", 0.0),
            "metadata": {
                "original_fields": extracted_data
            }
        }
        return ExpenseSchema(**normalized)

    def normalize_receipt(self, extracted_data: Dict[str, Any]) -> ExpenseSchema:
        normalized = {
            "source_type": "receipt",
            "vendor": extracted_data.get("merchant", ""),
            "date": None,  # Receipts may not always have a date
            "total_amount": self._parse_amount(extracted_data.get("total")),
            "line_items": self._normalize_receipt_items(extracted_data.get("items", [])),
            "tax_amount": self._parse_amount(extracted_data.get("tax")),
            "currency": "USD",
            "confidence": extracted_data.get("confidence", 0.0),
            "metadata": {
                "original_fields": extracted_data
            }
        }
        return ExpenseSchema(**normalized)

    def _parse_date(self, date_str: Optional[str]) -> Optional[str]:
        if not date_str:
            return None
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed_date.isoformat()
        except (ValueError, TypeError):
            return None

    def _parse_amount(self, amount_str: Optional[str]) -> Optional[float]:
        if not amount_str:
            return None
        try:
            return float(amount_str.replace(",", "").replace("$", ""))
        except (ValueError, AttributeError):
            return None

    def _normalize_line_items(self, line_items: list) -> list:
        normalized_items = []
        for item in line_items:
            normalized_item = {
                "description": item.get("description", ""),
                "quantity": self._parse_quantity(item.get("quantity")),
                "unit_price": self._parse_amount(item.get("unit_price")),
                "amount": self._parse_amount(item.get("amount"))
            }
            normalized_items.append(normalized_item)
        return normalized_items

    def _normalize_receipt_items(self, items: list) -> list:
        normalized_items = []
        for item in items:
            normalized_item = {
                "description": item.get("description", ""),
                "quantity": self._parse_quantity(item.get("quantity")),
                "unit_price": self._parse_amount(item.get("price")),
                "amount": self._parse_amount(item.get("amount"))
            }
            normalized_items.append(normal_item)
        return normalized_items

    def _parse_quantity(self, quantity_str: Optional[str]) -> Optional[float]:
        if not quantity_str:
            return None
        try:
            return float(quantity_str)
        except (ValueError, TypeError):
            return None