from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import OcrResponse, DocumentBlock, BlockType, BoundingBox, DocumentTable


class LayoutExtractor:
    def __init__(self):
        self.client = DocumentClient()

    def extract_layout(self, file_path: str) -> OcrResponse:
        with open(file_path, "rb") as file:
            file_stream = file.read()

        result = self.client.analyze_document(
            model_id="prebuilt-layout", file_stream=file_stream
        )

        text = result.get("content", "")
        blocks = []
        tables = []

        for paragraph in result.get("paragraphs", []):
            bounding_box = None
            if "boundingRegions" in paragraph and paragraph["boundingRegions"]:
                vertices = [
                    {"x": point["x"], "y": point["y"]}
                    for point in paragraph["boundingRegions"][0]["polygon"]
                ]
                bounding_box = BoundingBox(vertices=vertices)

            block = DocumentBlock(
                block_type=BlockType.PARAGRAPH,
                text=paragraph.get("content"),
                bounding_box=bounding_box,
                confidence=paragraph.get("confidence"),
            )
            blocks.append(block)

        for table in result.get("tables", []):
            rows = table.get("rowCount", 0)
            cols = table.get("columnCount", 0)
            cells = []

            for cell in table.get("cells", []):
                cell_bbox = None
                if "boundingRegions" in cell and cell["boundingRegions"]:
                    vertices = [
                        {"x": point["x"], "y": point["y"]}
                        for point in cell["boundingRegions"][0]["polygon"]
                    ]
                    cell_bbox = BoundingBox(vertices=vertices)

                cells.append({
                    "row_index": cell.get("rowIndex"),
                    "column_index": cell.get("columnIndex"),
                    "text": cell.get("content"),
                    "bounding_box": cell_bbox,
                })

            table_bbox = None
            if "boundingRegions" in table and table["boundingRegions"]:
                vertices = [
                    {"x": point["x"], "y": point["y"]}
                    for point in table["boundingRegions"][0]["polygon"]
                ]
                table_bbox = BoundingBox(vertices=vertices)

            tables.append(
                DocumentTable(
                    rows=rows, cols=cols, cells=cells, bounding_box=table_bbox
                )
            )

        return OcrResponse(text=text, blocks=blocks, tables=tables, key_value_pairs=[])