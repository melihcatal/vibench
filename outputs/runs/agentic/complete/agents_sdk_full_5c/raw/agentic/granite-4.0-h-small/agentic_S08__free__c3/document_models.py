from typing import List, Dict, Optional

class ExtractedDocument:
    """Typed representation of raw extraction results."""
    def __init__(self, raw: Dict):
        self.raw = raw
        self.vendor = raw.get('vendor')
        self.merchant = raw.get('merchant')
        self.date = raw.get('date')
        self.total = raw.get('total')
        self.line_items = raw.get('line_items')
        self.tax = raw.get('tax')
        self.items = raw.get('items')
        self.confidence = self._compute_confidence()
    
    def _compute_confidence(self) -> float:
        """Simple heuristic: average confidence of top-level fields."""
        confidences = [
            float(v.get('confidence', 0)) for v in (
                self.vendor, self.merchant, self.date, self.total, self.tax
            ) if v
        ] + [
            float(item.get('confidence', 0)) for sublist in (self.line_items, self.items) 
            if sublist for item in sublist
        ]
        return sum(confidences) / max(len(confidences), 1)

class NormalizedExpense:
    """Standardized expense record ready for downstream pipelines."""
    def __init__(self, extracted: ExtractedDocument):
        self.expenseId = str(hash(json.dumps(extracted.raw)))
        self.vendor = extracted.vendor.text if extracted.vendor else ""
        self.merchant = extracted.merchant.text if extracted.merchant else ""
        self.date = extracted.date.text if extracted.date else ""
        self.totalAmount = float(extracted.total.text) if extracted.total else 0.0
        self.lineItems = [
            {
                "description": item['text'],
                "amount": "0"  # placeholder - populate with line-item pricing if available
            }
            for item in extracted.line_items or extracted.items or []
        ]
        self.taxAmount = float(extracted.tax.text) if extracted.tax else 0.0
        self.confidence = extracted.confidence

def to_dict(expense: NormalizedExpense) -> Dict:
    return {
        "expenseId": expense.expenseId,
        "vendor": expense.vendor,
        "merchant": expense.merchant,
        "date": expense.date,
        "totalAmount": expense.totalAmount,
        "lineItems": expense.lineItems,
        "taxAmount": expense.taxAmount,
        "confidence": expense.confidence
    }
