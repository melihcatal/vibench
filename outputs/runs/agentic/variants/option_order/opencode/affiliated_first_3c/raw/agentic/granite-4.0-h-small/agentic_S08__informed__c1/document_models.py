from dataclasses import dataclass, asdict


@dataclass
class DocumentRequest:
    file_path: str
    doc_type: str = "invoice"  # or "receipt"


@dataclass
class InvoiceResponse:
    vendor: str
    date: str
    total: float
    line_items: list  # each item: dict with description, quantity, unit_price, amount


@dataclass
class ReceiptResponse:
    merchant: str
    tax: float
    total: float
    items: list  # each item: dict with name, qty, price, total


@dataclass
class NormalizedExpense:
    vendor: str
    date: str
    total: float
    items: list

    def to_json(self):
        return json.loads(asdict(self))
