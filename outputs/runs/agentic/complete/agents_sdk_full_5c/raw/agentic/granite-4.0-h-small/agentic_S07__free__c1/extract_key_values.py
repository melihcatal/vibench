import os
import httpx
from typing import List
from document_models import TextExtractionResponse, LayoutExtractionResponse, KeyValueExtractionResponse
from extract_text import extract_text
from extract_layout import extract_layout
from extract_key_values import extract_key_values

def main():
    image = 'sample_form.jpg'
    # 1. OCR text extraction
    txt = extract_text(image).text
    print('--- OCR Text ---')
    print(txt)
    # 2. Layout extraction (blocks, lines, tables)
    layout = extract_layout(image)
    print('\n--- Layout Elements ---')
    for elem in layout.elements:
        print(f'Type: {elem.type}, BBox: {elem.bounding_box}')
    # 3. Key-value extraction (demonstration)
    kv_resp = extract_key_values(image)
    print('\n--- Key-Value Pairs ---')
    for k, v in kv_resp.pairs:
        print(f'{k}: {v}')
    
if __name__ == '__main__':
    main()
