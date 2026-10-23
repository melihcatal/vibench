from document_client import image_from_content, vision_client
from document_models import DocumentRequest


def extract_tables(request: DocumentRequest) -> list[dict]:
    client = vision_client()
    response = client.document_text_detection(image=image_from_content(request.content))
    tables: list[dict] = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    if word.symbols:
                        tables.append({"cells": ["".join(symbol.text for symbol in word.symbols)], "rows": 1})
    return tables
