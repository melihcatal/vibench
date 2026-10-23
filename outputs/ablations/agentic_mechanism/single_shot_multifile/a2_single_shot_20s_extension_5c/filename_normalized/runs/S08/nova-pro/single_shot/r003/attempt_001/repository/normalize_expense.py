import os
from google.cloud import documentai

def normalize_expense(fields):
    normalized = {}
    normalized['vendor'] = fields.get('vendor')
    normalized['date'] = fields.get('date')
    normalized['total'] = fields.get('total')
    normalized['line_items'] = fields.get('line_items', [])
    normalized['merchant'] = fields.get('merchant')
    normalized['tax'] = fields.get('tax')
    normalized['items'] = fields.get('items', [])
    return normalized