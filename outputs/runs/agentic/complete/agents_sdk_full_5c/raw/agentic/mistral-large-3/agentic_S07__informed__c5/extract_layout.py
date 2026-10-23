from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import DocumentLayout, DocumentElement, BoundingBox, BlockType


class LayoutExtractor:
    def __init__(self):
        self.client = DocumentClient()

    def extract_layout(self, file_path: str) -> DocumentLayout:
        result = self.client.analyze_document(file_path)
        elements = self._parse_elements(result)
        tables = self._parse_tables(result)
        key_value_pairs = self._parse_key_values(result)
        return DocumentLayout(elements=elements, tables=tables, key_value_pairs=key_value_pairs)

    def _parse_elements(self, result: Dict[str, Any]) -> List[DocumentElement]:
        elements = []
        for paragraph in result.get("paragraphs", []):
            bounding_box = self._parse_bounding_box(paragraph.get("boundingRegions", [{}])[0].get("polygon"))
            elements.append(
                DocumentElement(
                    text=paragraph.get("content", ""),
                    block_type=BlockType.PARAGRAPH,
                    bounding_box=bounding_box,
                    confidence=paragraph.get("confidence", 0.0),
                )
            )
        for line in result.get("lines", []):
            bounding_box = self._parse_bounding_box(line.get("boundingRegions", [{}])[0].get("polygon"))
            elements.append(
                DocumentElement(
                    text=line.get("content", ""),
                    block_type=BlockType.LINE,
                    bounding_box=bounding_box,
                    confidence=line.get("confidence", 0.0),
                )
            )
        return elements

    def _parse_bounding_box(self, polygon: List[Dict[str, float]]) -> BoundingBox:
        if not polygon:
            return BoundingBox(0.0, 0.0, 0.0, 0.0)
        x_coords = [point.get("x", 0.0) for point in polygon]
        y_coords = [point.get("y", 0.0) for point in polygon]
        return BoundingBox(
            x_min=min(x_coords),
            y_min=min(y_coords),
            x_max=max(x_coords),
            y_max=max(y_coords),
        )

    def _parse_tables(self, result: Dict[str, Any]) -> List:
        return []  # Tables are parsed in extract_tables.py

    def _parse_key_values(self, result: Dict[str, Any]) -> List:
        return []  # Key-values are parsed in extract_key_values.py