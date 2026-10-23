from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_id: str
    text: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class FieldItem:
    description: str
    amount: Optional[float] = None
    quantity: Optional[float] = None
    confidence: Optional[float] = None


@dataclass
class DocumentResponse:
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    notes: Optional[str] = None
    items: Optional[List[FieldItem]] = None


def request_to_dict(request: DocumentRequest) -> Dict[str, Any]:
    return asdict(request)


def response_to_dict(response: DocumentResponse) -> Dict[str, Any]:
    data = asdict(response)
    if data.get("items"):
        data["items"] = [asdict(item) for item in data["items"]]
    return data


def standard_expense_schema(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": response.get("vendor") or response.get("merchant"),
        "date": response.get("date"),
        "total": response.get("total"),
        "tax": response.get("tax"),
        "notes": response.get("notes"),
        "items": response.get("items", []),
    }
