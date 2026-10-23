from __future__ import annotations

class DocumentModel:
    def __init__(self, vendor=None, date=None, total=None, line_items=None, confidence=None):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items or []
        self.confidence = confidence
    def to_json(self) -> dict:
        return {
            'vendor': self.vendor,
            'date': self.date,
            'total': self.total,
            'line_items': self.line_items,
            'confidence': self.confidence
        }
