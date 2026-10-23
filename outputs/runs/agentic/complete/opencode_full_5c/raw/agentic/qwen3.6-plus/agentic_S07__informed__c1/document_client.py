import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")


def get_di_client():
    credential = AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY)
    client = DocumentIntelligenceClient(
        endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
        credential=credential,
    )
    return client


def read_image_bytes(image_path):
    with open(image_path, "rb") as f:
        return f.read()


def read_image_bytes_from_bytes(image_bytes):
    return image_bytes


def parse_di_response_to_text(result):
    content = result.content if hasattr(result, "content") else ""
    return content.strip()


def parse_di_response_to_blocks(result):
    blocks = []
    if hasattr(result, "paragraphs") and result.paragraphs:
        for para in result.paragraphs:
            blocks.append(
                {
                    "type": "paragraph",
                    "content": para.content,
                    "bounding_regions": [
                        {"page_number": r.page_number, "polygon": r.polygon}
                        for r in (para.bounding_regions or [])
                    ],
                }
            )
    if hasattr(result, "tables") and result.tables:
        for table in result.tables:
            blocks.append(
                {
                    "type": "table",
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                    "bounding_regions": [
                        {"page_number": r.page_number, "polygon": r.polygon}
                        for r in (table.bounding_regions or [])
                    ],
                }
            )
    return blocks


def parse_di_response_to_tables(result):
    tables = []
    if hasattr(result, "tables") and result.tables:
        for table in result.tables:
            cells = []
            if table.cells:
                for cell in table.cells:
                    cells.append(
                        {
                            "row_index": cell.row_index,
                            "column_index": cell.column_index,
                            "content": cell.content,
                            "row_span": cell.row_span,
                            "column_span": cell.column_span,
                            "bounding_regions": [
                                {"page_number": r.page_number, "polygon": r.polygon}
                                for r in (cell.bounding_regions or [])
                            ],
                        }
                    )
            tables.append(
                {
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                    "cells": cells,
                    "bounding_regions": [
                        {"page_number": r.page_number, "polygon": r.polygon}
                        for r in (table.bounding_regions or [])
                    ],
                }
            )
    return tables


def parse_di_response_to_key_values(result):
    key_values = []
    if hasattr(result, "key_value_pairs") and result.key_value_pairs:
        for kv in result.key_value_pairs:
            key_content = kv.key.content if kv.key else ""
            value_content = kv.value.content if kv.value else ""
            key_values.append(
                {
                    "key": key_content,
                    "value": value_content,
                    "confidence": kv.confidence,
                }
            )
    return key_values
