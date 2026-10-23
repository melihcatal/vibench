from dataclasses import dataclass
from typing import Any, Dict

def _get(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

@dataclass
class DocumentRequest:
    content: Any
    content_type: str | None = None
    metadata: Dict[str, Any] | None = None
    @classmethod
    def from_input(cls, request):
        if isinstance(request, cls):
            return request
        if isinstance(request, dict):
            return cls(content=request.get('content') or request.get('document') or request.get('bytes'), content_type=request.get('content_type') or request.get('mime_type'), metadata=request.get('metadata') or {})
        return cls(content=getattr(request, 'content', request), content_type=getattr(request, 'content_type', None), metadata=getattr(request, 'metadata', {}) or {})

@dataclass
class DocumentResponse:
    provider: str
    document_type: str
    fields: Dict[str, Any]
    def to_dict(self):
        return {'provider': self.provider, 'document_type': self.document_type, 'fields': self.fields}

@dataclass
class NormalizedExpense:
    vendor: str | None = None
    document_date: str | None = None
    total_amount: float | None = None
    currency: str | None = None
    line_items: list | None = None
    @classmethod
    def from_payload(cls, payload):
        fields = payload.get('fields', payload) if isinstance(payload, dict) else {}
        return cls(vendor=_get(fields, 'vendor'), document_date=_get(fields, 'date') if not isinstance(_get(fields, 'date'), dict) else _get(_get(fields, 'date'), 'value'), total_amount=None if _get(fields, 'total') is None else float(str(_get(_get(fields, 'total'), 'value') if isinstance(_get(fields, 'total'), dict) else _get(fields, 'total')).replace('$','').replace(',','')), currency=_get(payload, 'currency') or 'USD', line_items=_get(fields, 'line_items') or [])
    def to_dict(self):
        return {'vendor': self.vendor, 'document_date': self.document_date, 'total_amount': self.total_amount, 'currency': self.currency, 'line_items': self.line_items or []}

def normalize_expense_payload(request):
    return request if isinstance(request, dict) else getattr(request, '__dict__', {})

def validate_document_payload(request):
    payload = request if isinstance(request, dict) else getattr(request, '__dict__', {})
    fields = payload.get('fields', payload)
    required = ['vendor', 'date', 'total']
    missing = [r for r in required if not fields.get(r)]
    confidences = {k: (v.get('confidence') if isinstance(v, dict) else None) for k, v in fields.items() if isinstance(v, dict)}
    return {'valid': not missing, 'missing_fields': missing, 'confidence_scores': confidences}
