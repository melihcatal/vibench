from typing import Any, Dict, Iterable


def _kv(fields: Any) -> Dict[str, Any]:
    if not fields:
        return {}
    return {k: getattr(v, 'value', getattr(v, 'content', None)) for k, v in fields.items()}


def _confidence(fields: Any) -> Dict[str, float]:
    if not fields:
        return {}
    out = {}
    for k, v in fields.items():
        conf = getattr(v, 'confidence', None)
        if conf is not None:
            out[k] = conf
    return out


def extract_invoice_result(result: Any) -> Dict[str, Any]:
    docs = getattr(result, 'documents', []) or []
    doc = docs[0] if docs else None
    fields = getattr(doc, 'fields', {}) if doc else {}
    return {'vendor': _kv(fields).get('VendorName') or _kv(fields).get('Vendor'), 'date': _kv(fields).get('InvoiceDate'), 'total': _kv(fields).get('InvoiceTotal'), 'line_items': _kv(fields).get('Items', []), 'confidence': _confidence(fields)}


def extract_receipt_result(result: Any) -> Dict[str, Any]:
    docs = getattr(result, 'documents', []) or []
    doc = docs[0] if docs else None
    fields = getattr(doc, 'fields', {}) if doc else {}
    return {'merchant': _kv(fields).get('MerchantName'), 'tax': _kv(fields).get('Tax'), 'total': _kv(fields).get('Total'), 'items': _kv(fields).get('Items', []), 'confidence': _confidence(fields)}


def normalize_expense_schema(result: Any) -> Dict[str, Any]:
    docs = getattr(result, 'documents', []) or []
    doc = docs[0] if docs else None
    fields = getattr(doc, 'fields', {}) if doc else {}
    kv = _kv(fields)
    return {'merchant': kv.get('VendorName') or kv.get('MerchantName'), 'date': kv.get('InvoiceDate') or kv.get('TransactionDate'), 'currency': kv.get('CurrencyCode'), 'amount': kv.get('InvoiceTotal') or kv.get('Total'), 'memo': kv.get('Description'), 'source': 'azure-document-intelligence'}


def validate_structured_fields(result: Any) -> Dict[str, Any]:
    docs = getattr(result, 'documents', []) or []
    doc = docs[0] if docs else None
    fields = getattr(doc, 'fields', {}) if doc else {}
    kv = _kv(fields)
    confidence = _confidence(fields)
    required = ['InvoiceDate', 'InvoiceTotal']
    missing = [x for x in required if x not in kv or kv.get(x) in (None, '')]
    low_confidence = [k for k, v in confidence.items() if v < 0.8]
    return {'valid': not missing and not low_confidence, 'missing': missing, 'low_confidence': low_confidence, 'confidence': confidence}
