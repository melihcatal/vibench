from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import OcrResponse, KeyValuePair, DocumentBlock, BlockType, BoundingBox


class KeyValueExtractor:
    def __init__(self):
        self.client = DocumentClient()

    def extract_key_values(self, file_path: str) -> OcrResponse:
        with open(file_path, "rb") as file:
            file_stream = file.read()

        result = self.client.analyze_document(
            model_id="prebuilt-layout", file_stream=file_stream
        )

        key_value_pairs = []

        for kv_pair in result.get("keyValuePairs", []):
            key_bbox = None
            if kv_pair.get("key", {}).get("boundingRegions"):
                vertices = [
                    {"x": point["x"], "y": point["y"]}
                    for point in kv_pair["key"]["boundingRegions"][0]["polygon"]
                ]
                key_bbox = BoundingBox(vertices=vertices)

            value_bbox = None
            if kv_pair.get("value", {}).get("boundingRegions"):
                vertices = [
                    {"x": point["x"], "y": point["y"]}
                    for point in kv_pair["value"]["boundingRegions"][0]["polygon"]
                ]
                value_bbox = BoundingBox(vertices=vertices)

            key_block = DocumentBlock(
                block_type=BlockType.WORD,
                text=kv_pair.get("key", {}).get("content"),
                bounding_box=key_bbox,
                confidence=kv_pair.get("confidence"),
            )

            value_block = DocumentBlock(
                block_type=BlockType.WORD,
                text=kv_pair.get("value", {}).get("content"),
                bounding_box=value_bbox,
                confidence=kv_pair.get("confidence"),
            )

            key_value_pairs.append(
                KeyValuePair(key=key_block, value=value_block, confidence=kv_pair.get("confidence"))
            )

        return OcrResponse(text="", blocks=[], tables=[], key_value_pairs=key_value_pairs)