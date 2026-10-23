import os
from google.cloud import documentai_v1 as documentai
import re

def extract_fields_from_text(text: str) -> dict:
    # Example: find key/value pairs separated by a colon
    kv = {}
    for line in text.splitlines():
        m = re.match(r'([^:\s]+):\s*(.*)', line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip()
            kv[key] = value
    # Example: detect invoice number pattern
    invoice = re.search(r'Invoice\s*Number:\s*(\w+)', text, re.IGNORECASE)
    if invoice:
        kv['invoice_number'] = invoice.group(1).strip()
    # Add any other domain-specific patterns here
    return kv
