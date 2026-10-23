import os
import httpx
from typing import List
from document_models import EmbeddingRequest, EmbeddingResponse
from ocr_embedding import embed_via_hosted_api

def main():
    # Simulated OCR output split into meaningful chunks
    sample_texts = [
        'Invoice Number: 12345\nDate: 2024-01-15\nAmount: $1,250.00\nPurpose: Office Supplies',
        'Vendor: Acme Corp\nAddress: 123 Main St, Anytown\nContact: John Doe',
        'Line Item 1: 10 pens @ $0.50 each = $5.00\nLine Item 2: 5 notebooks @ $2.00 each = $10.00'
    ]
    response: EmbeddingResponse = embed_via_hosted_api(EmbeddingRequest(texts=sample_texts))
    print('--- Embeddings ---')
    for i, emb in enumerate(response.embeddings):
        print(f'Section {i+1} embedding length: {len(emb)}')
    # Embeddings can now be stored, indexed, or queried for similarity

if __name__ == '__main__':
    main()
