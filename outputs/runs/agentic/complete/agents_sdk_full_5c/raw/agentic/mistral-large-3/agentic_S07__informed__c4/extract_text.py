import os
from typing import Dict, Any
from document_client import DocumentClient
from document_models import OcrResponse, DocumentBlock, BlockType


class TextExtractor:
    def __init__(self):
        self.client = DocumentClient()

    def extract_text(self, file_path: str) -> OcrResponse:
        with open(file_path, "rb") as file:
            file_stream = file.read()

        result = self.client.analyze_document(
            model_id="prebuilt-read", file_stream=file_stream
        )

        text = result.get("content", "")
        blocks = []

        for paragraph in result.get("paragraphs", []):
            block = DocumentBlock(
                block_type=BlockType.PARAGRAPH,
                text=paragraph.get("content"),
                bounding_box=None,
                confidence=paragraph.get("confidence"),
            )
            blocks.append(block)

        return OcrResponse(text=text, blocks=blocks, tables=[], key_value_pairs=[])