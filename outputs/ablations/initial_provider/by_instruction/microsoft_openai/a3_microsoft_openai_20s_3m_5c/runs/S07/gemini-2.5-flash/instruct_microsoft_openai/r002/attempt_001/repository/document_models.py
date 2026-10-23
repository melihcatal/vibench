from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class DocumentText:
    content: str
    language: str = "en"

@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float

@dataclass
class DocumentBlock:
    text: str
    bounding_box: BoundingBox
    block_type: str # e.g., "paragraph", "title", "list_item"

@dataclass
class DocumentTable:
    rows: List[List[Dict[str, Any]]]
    bounding_box: BoundingBox = field(default_factory=lambda: BoundingBox(0,0,0,0)) # Placeholder

@dataclass
class DocumentField:
    field_name: str
    field_value: str
    confidence: float
    bounding_box: BoundingBox = field(default_factory=lambda: BoundingBox(0,0,0,0)) # Placeholder

@dataclass
class DocumentLayout:
    blocks: List[DocumentBlock] = field(default_factory=list)
    tables: List[DocumentTable] = field(default_factory=list)
    key_values: List[DocumentField] = field(default_factory=list)

def normalize_azure_vision_text_response(azure_response: Any) -> DocumentText:
    """
    Normalizes the response from Azure AI Vision text extraction.
    """
    # This is a simplified normalization. In a real scenario, you'd parse
    # the result object from Azure AI Vision carefully.
    extracted_text = ""
    if hasattr(azure_response, 'read_result') and azure_response.read_result:
        for page in azure_response.read_result.pages:
            for line in page.lines:
                extracted_text += line.text + "\n"
    elif isinstance(azure_response, str): # if we passed a dummy string
        extracted_text = azure_response
    
    return DocumentText(content=extracted_text.strip())

def normalize_azure_document_intelligence_layout_response(azure_response: Any) -> DocumentLayout:
    """
    Normalizes the response from Azure AI Document Intelligence layout extraction.
    """
    layout = DocumentLayout()
    if azure_response and hasattr(azure_response, 'pages'):
        for page in azure_response.pages:
            for line in page.lines:
                # Simplified block creation for demonstration
                layout.blocks.append(DocumentBlock(
                    text=line.content,
                    bounding_box=BoundingBox(line.bounding_box[0], line.bounding_box[1], line.bounding_box[4], line.bounding_box[5]),
                    block_type="line"
                ))
        if hasattr(azure_response, 'tables'):
            for azure_table in azure_response.tables:
                rows_data = []
                for cell in azure_table.cells:
                    while len(rows_data) <= cell.row_index:
                        rows_data.append([])
                    while len(rows_data[cell.row_index]) <= cell.column_index:
                        rows_data[cell.row_index].append({"content": ""})
                    rows_data[cell.row_index][cell.column_index]["content"] = cell.content
                
                # Create a simplified bounding box for the table
                table_bbox_coords = azure_table.bounding_regions[0].bounding_box if azure_table.bounding_regions else [0,0,0,0,0,0,0,0]
                table_bbox = BoundingBox(
                    table_bbox_coords[0], table_bbox_coords[1], 
                    table_bbox_coords[4], table_bbox_coords[5]
                )
                layout.tables.append(DocumentTable(rows=rows_data, bounding_box=table_bbox))

    if azure_response and hasattr(azure_response, 'fields'):
        for field_name, field_value in azure_response.fields.items():
            if field_value:
                value_content = field_value.content if hasattr(field_value, 'content') else str(field_value.value)
                confidence = field_value.confidence if hasattr(field_value, 'confidence') else 1.0

                # Simplified bounding box for the field
                field_bbox = BoundingBox(0,0,0,0)
                if hasattr(field_value, 'bounding_regions') and field_value.bounding_regions:
                    bbox_coords = field_value.bounding_regions[0].bounding_box
                    field_bbox = BoundingBox(bbox_coords[0], bbox_coords[1], bbox_coords[4], bbox_coords[5])

                layout.key_values.append(DocumentField(
                    field_name=field_name,
                    field_value=value_content,
                    confidence=confidence,
                    bounding_box=field_bbox
                ))

    return layout
