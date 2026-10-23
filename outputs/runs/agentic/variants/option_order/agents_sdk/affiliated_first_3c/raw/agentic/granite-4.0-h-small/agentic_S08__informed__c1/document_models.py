from typing import List, Dict

Invoice = Dict[str, any]
Receipt = Dict[str, any]
NormalizedExpense = Dict[str, any]

# Simple helper to bundle related data structures used across files
# In a larger system these could be actual data classes or Pydantic models

class DocumentModels:
    @staticmethod
    def as_invoice(raw: Invoice) -> Invoice:
        return raw

    @staticmethod
    def as_receipt(raw: Receipt) -> Receipt:
        return raw

    @staticmethod
    def normalize(expense: Invoice or Receipt) -> NormalizedExpense:
        return {
            'vendor': expense.get('vendor') or expense.get('merchant'),
            'date': expense.get('date'),
            'total': float(expense.get('total') or 0),
            'line_items': []
        }

    # No concrete validation logic - clients should use validate_document_fields.py
