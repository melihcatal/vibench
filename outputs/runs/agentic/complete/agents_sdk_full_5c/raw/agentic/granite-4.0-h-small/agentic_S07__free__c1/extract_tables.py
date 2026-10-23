import os
import httpx
from typing import List
from document_models import TextExtractionResponse, KeyValueExtractionResponse, TableExtractionResponse
from extract_text import extract_text
from extract_tables import extract_tables
from extract_key_values import extract_key_values

def main():
    image = 'sample_invoice.jpg'
    # 1. OCR text extraction
    txt = extract_text(image).text
    print('--- OCR Text ---')
    print(txt)
    # 2. Extract tables
    tables = extract_tables(image)
    print('\n--- Extracted Tables ---')
    for row in tables.rows:
        cells = [cell.content for cell in row.cells]
        print(cells)
    # 3. Extract key-value pairs
    kv_resp = extract_key_values(image)
    print('\n--- Key-Value Pairs ---')
    for k, v in kv_resp.pairs:
        print(f'{k}: {v}')
    # 4. Layout extraction (demonstration)
    # from extract_layout import extract_layout  # not called in this demo
    
if __name__ == '__main__':
    main()
