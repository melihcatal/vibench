import os
from typing import List
from ocr_embedding import embed_sections
from document_models import EmbeddingRequest

def get_doc_sections(text: str) -> List[str]:
    """Simple heuristic to split document into logical sections."""
    # Split on double newlines, filter empty
    return [section.strip() for section in text.split('\n\n') if section.strip()]

def main():
    # Example: embedding a multi‑page report saved as plain‑text (simulating OCR output)
    with open('report.txt', 'r', encoding='utf-8') as f:
        document_text = f.read()
    sections = get_doc_sections(document_text)
    embeddings = embed_sections(sections)
    print('--- Embeddings (shape) ---')
    for i, emb in enumerate(embeddings):
        print(f'Section {i+1} embedding size: {len(emb)}')
    # Further usage: store embeddings, index for retrieval, etc.

if __name__ == '__main__':
    main()
