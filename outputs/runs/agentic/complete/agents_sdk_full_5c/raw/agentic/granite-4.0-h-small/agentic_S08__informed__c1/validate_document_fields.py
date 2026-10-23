import os
import boto3
from document_models import InvoiceDocument
from validate_document_fields import validate_document_fields

# Validate required fields and confidence scores for an invoice

def validate_document_fields(data: dict) -> dict:
    required_fields = ['vendor', 'date', 'total', 'line_items']
    missing = [f for f in required_fields if f not in data]
    low_conf = []
    if 'total' in data and (not isinstance(data['total'], (int, float)) or data['total'] <= 0):
        low_conf.append('total')
    return {
        'is_valid': len(missing) == 0,
        'missing_fields': missing,
        'low_confidence': low_conf
    }
