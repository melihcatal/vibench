from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ExtractedText:
    content: str

@dataclass
class ExtractedTableBodyRow:
    cells: List[str]

@dataclass
class ExtractedTable:
    headers: List[str]
    body_rows: List[ExtractedTableBodyRow]
    page_number: int

@dataclass
class ExtractedKeyValuePair:
    key: str
    value: str
    page_number: int

@dataclass
class ExtractedDocumentLayout:
    text: str
    tables: List[ExtractedTable]
    key_value_pairs: List[ExtractedKeyValuePair]
    # Add other layout elements as needed, e.g., blocks, paragraphs, etc.


# Example normalization function (simplified)
def normalize_documentai_document(document: Any) -> ExtractedDocumentLayout:
    """
    Normalizes a Google Document AI Document object into a simpler structure.
    This is a highly simplified example.
    """
    extracted_tables = []
    extracted_key_values = []

    if document.pages:
        for page_idx, page in enumerate(document.pages):
            for table in page.tables:
                headers = [cell.layout.text_anchor.content for row in table.header_rows for cell in row.cells if cell.layout.text_anchor.content]
                body_rows = []
                for row in table.body_rows:
                    body_rows.append(ExtractedTableBodyRow(cells=[cell.layout.text_anchor.content for cell in row.cells if cell.layout.text_anchor.content]))
                extracted_tables.append(ExtractedTable(headers=headers, body_rows=body_rows, page_number=page_idx + 1))

    if document.entities:
        for entity in document.entities:
            if entity.type_ == "form_field" and entity.text_anchor:
                key = entity.text_anchor.content # Simplified key extraction
                value = entity.normalized_value.text if entity.normalized_value else (entity.properties[0].text_anchor.content if entity.properties else "") # Simplified value extraction
                # Determine page number for key-value pair, simplified to 1 for this example
                page_number = 1 
                extracted_key_values.append(ExtractedKeyValuePair(key=key, value=value, page_number=page_number))

    return ExtractedDocumentLayout(
        text=document.text,
        tables=extracted_tables,
        key_value_pairs=extracted_key_values
    )


if __name__ == '__main__':
    print("Document models and normalization helpers defined.")
