import re
from typing import Dict, List
from document_models import LayoutResult, TableCellResult, TableResult

# Simple utility to map form-like key/value pairs using regex patterns

KEY_VALUE_PATTERNS = {
    'INVOICE_NUMBER': r'Invoice[\s_-]?Number[:\s_-]?([A-Z0-9-]+)',
    'DATE': r'Date[:\s_-]?([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})',
    'TOTAL': r'Total[:\s_-]?[$]([0-9,]+(?:\.[0-9]{2})?)',
}

def extract_fields_from_layout(layout: LayoutResult) -> Dict[str, str]:
    '''
    Extract structured fields from OCR-normalized layout result.
    Currently handles plain lines and simple regex patterns.
    '''
    fields = {}
    # Search through lines first
    for line in layout.get('lines', []):
        for key, pattern in KEY_VALUE_PATTERNS.items():
            m = re.search(pattern, line, re.IGNORECASE)
            if m and key not in fields:
                fields[key] = m.group(1).strip()
    # Fallback: scan table cells for a header row
    for table in layout.get('tables', []):
        if not table:
            continue
        header_row = table[0]
        data_rows = table[1:]
        headers = [cell['text'] for cell in header_row if isinstance(cell, TableCellResult)]
        for row in data_rows:
            for i, cell in enumerate(row):
                if cell.get('text') and headers[i]:
                    key = headers[i].upper()
                    pattern = KEY_VALUE_PATTERNS.get(key)
                    if pattern and key not in fields:
                        m = re.search(pattern, cell['text'], re.IGNORECASE)
                        if m:
                            fields[key] = m.group(1).strip()
    return fields
