from typing import Any, Callable, Dict, List


def _expense_fields(expense: Dict[str, Any], normalize_text: Callable[[Any], str]) -> Dict[str, Any]:
    fields = expense.get('SummaryFields', []) or []
    line_items = expense.get('LineItemGroups', []) or []
    result = {'vendor': '', 'date': '', 'total': '', 'items': []}
    for field in fields:
        key = normalize_text(field.get('Type', {}).get('Text', '')).lower()
        val = field.get('ValueDetection', {}).get('Text', '')
        if key in {'vendor', 'merchant'}:
            result['vendor'] = normalize_text(val)
        elif key in {'invoice receipt date', 'date'}:
            result['date'] = normalize_text(val)
        elif key in {'total', 'amount due'}:
            result['total'] = normalize_text(val)
    for group in line_items:
        for line in group.get('LineItems', []) or []:
            item = {}
            for entry in line.get('LineItemExpenseFields', []) or []:
                name = normalize_text(entry.get('Type', {}).get('Text', '')).lower()
                value = normalize_text(entry.get('ValueDetection', {}).get('Text', ''))
                if name:
                    item[name] = value
            if item:
                result['items'].append(item)
    return result


def build_invoice_result(response: Dict[str, Any], normalize_text: Callable[[Any], str]) -> Dict[str, Any]:
    blocks = response.get('ExpenseDocuments', []) or []
    return _expense_fields(blocks[0] if blocks else {}, normalize_text)


def build_receipt_result(response: Dict[str, Any], normalize_text: Callable[[Any], str]) -> Dict[str, Any]:
    return build_invoice_result(response, normalize_text)


def normalize_expense_record(extracted: Dict[str, Any], normalize_text: Callable[[Any], str], confidence_score: Callable[[Any], float]) -> Dict[str, Any]:
    return {
        'vendor': normalize_text(extracted.get('vendor')),
        'date': normalize_text(extracted.get('date')),
        'total': normalize_text(extracted.get('total')),
        'items': extracted.get('items', []),
        'confidence': confidence_score(extracted.get('confidence', 0)),
    }


def validate_required_fields(payload: Dict[str, Any], confidence_score: Callable[[Any], float]) -> Dict[str, Any]:
    required = ['vendor', 'date', 'total']
    missing = [key for key in required if not payload.get(key)]
    confidence = confidence_score(payload.get('confidence', 0))
    return {'valid': not missing and confidence >= 0.5, 'missing': missing, 'confidence': confidence}
