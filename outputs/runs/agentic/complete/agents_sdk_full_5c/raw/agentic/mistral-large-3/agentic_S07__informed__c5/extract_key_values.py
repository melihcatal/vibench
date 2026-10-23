from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import KeyValuePair, DocumentElement, BoundingBox, BlockType


class KeyValueExtractor:
    def __init__(self):
        self.client = DocumentClient()

    def extract_key_values(self, file_path: str) -> List[KeyValuePair]:
        result = self.client.analyze_document(file_path)
        key_value_pairs = []
        for kv_pair in result.get("keyValuePairs", []):
            key = self._create_document_element(kv_pair.get("key", {}))
            value = self._create_document_element(kv_pair.get("value", {}))
            if key and value:
                key_value_pairs.append(
                    KeyValuePair(
                        key=key,
                        value=value,
                        confidence=kv_pair.get("confidence", 0.0),
                    )
                )
        return key_value_pairs

    def _create_document_element(self, element_data: Dict[str, Any]) -> DocumentElement:
        if not element_data:
            return None
        bounding_box = self._parse_bounding_box(element_data.get("boundingRegions", [{}])[0].get("polygon"))
        return DocumentElement(
            text=element_data.get("content", ""),
            block_type=BlockType.WORD,
            bounding_box=bounding_box,
            confidence=element_data.get("confidence", 0.0),
        )

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