from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def confidence_from_field(field: Any) -> Optional[float]:
    return getattr(field, 'confidence', None)


def normalize_line_items(items: Any) -> List[Dict[str, Any]]:
    normalized = []
    if not items:
        return normalized
    for item in items.value if hasattr(items, 'value') else items:
        fields = getattr(item, 'fields', {})
        normalized.append({k: getattr(v, 'value', v) for k, v in fields.items()})
    return normalized


def normalize_expense_record(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'vendor': payload.get('vendor') or payload.get('merchant'),
        'date': payload.get('date') or payload.get('transaction_date'),
        'total': payload.get('total'),
        'tax': payload.get('tax'),
        'items': payload.get('items') or payload.get('line_items', []),
        'currency': payload.get('currency', 'USD'),
        'confidence': payload.get('confidence', {}),
    }


def validate_required_fields(payload: Dict[str, Any], required: List[str]) -> Dict[str, Any]:
    missing = [field for field in required if payload.get(field) in (None, '', [], {})]
    confidence = payload.get('confidence', {})
    low_confidence = [field for field in required if confidence.get(field, 1.0) < 0.5]
    return {'valid': not missing and not low_confidence, 'missing': missing, 'low_confidence': low_confidence}
