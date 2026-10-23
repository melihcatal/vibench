from typing import Dict, Any, List
from google.cloud.documentai_v1 import Document

def normalize_document_text(document_json: str) -> Dict[str, Any]:
    # In a real application, this would parse the Document AI JSON
    # and extract normalized text, entities, tables, etc.
    # For this example, we'll just return the top-level text if available.
    document = Document.from_json(document_json)
    return {"text": document.text if document.text else ""}

def normalize_document_layout(document_json: str) -> Dict[str, Any]:
    document = Document.from_json(document_json)
    # This is a simplified representation. A real implementation would parse
    # pages, blocks, paragraphs, lines, etc.
    layout_data = {
        "pages": [],
        "document_text": document.text
    }
    for page in document.pages:
        page_info = {
            "page_number": page.page_number,
            "dimension": {"width": page.dimension.width, "height": page.dimension.height},
            "blocks": [],
            "lines": [],
            "paragraphs": []
        }
        for block in page.blocks:
            page_info["blocks"].append({"text": block.layout.text_anchor.content})
        for line in page.lines:
            page_info["lines"].append({"text": line.layout.text_anchor.content})
        for paragraph in page.paragraphs:
            page_info["paragraphs"].append({"text": paragraph.layout.text_anchor.content})
        layout_data["pages"].append(page_info)
    return layout_data

def normalize_document_tables(document_json: str) -> Dict[str, Any]:
    document = Document.from_json(document_json)
    tables_data = {
        "tables": [],
        "document_text": document.text
    }
    for page in document.pages:
        for table in page.tables:
            table_info = {
                "num_rows": table.num_rows,
                "num_columns": table.num_columns,
                "header_rows": [],
                "body_rows": []
            }
            for row in table.header_rows:
                row_cells = []
                for cell in row.cells:
                    row_cells.append({"text": cell.layout.text_anchor.content})
                table_info["header_rows"].append(row_cells)
            for row in table.body_rows:
                row_cells = []
                for cell in row.cells:
                    row_cells.append({"text": cell.layout.text_anchor.content})
                table_info["body_rows"].append(row_cells)
            tables_data["tables"].append(table_info)
    return tables_data

def normalize_document_key_values(document_json: str) -> Dict[str, Any]:
    document = Document.from_json(document_json)
    key_value_pairs = {
        "key_values": [],
        "document_text": document.text
    }
    for entity in document.entities:
        if entity.type_ == "form_field": # Assuming entities are form fields for KVs
            key = entity.mention_text
            value = entity.normalized_value.text if entity.normalized_value else entity.text_anchor.content
            key_value_pairs["key_values"].append({"key": key, "value": value})
    return key_value_pairs
