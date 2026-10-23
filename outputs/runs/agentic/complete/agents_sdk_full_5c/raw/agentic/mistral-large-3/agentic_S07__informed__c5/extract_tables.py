from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import DocumentTable, TableCell, BoundingBox


class TableExtractor:
    def __init__(self):
        self.client = DocumentClient()

    def extract_tables(self, file_path: str) -> List[DocumentTable]:
        result = self.client.analyze_document(file_path)
        tables = []
        for table in result.get("tables", []):
            cells = []
            for cell in table.get("cells", []):
                bounding_box = self._parse_bounding_box(cell.get("boundingRegions", [{}])[0].get("polygon"))
                cells.append(
                    TableCell(
                        row_index=cell.get("rowIndex", 0),
                        col_index=cell.get("columnIndex", 0),
                        row_span=cell.get("rowSpan", 1),
                        col_span=cell.get("columnSpan", 1),
                        text=cell.get("content", ""),
                        bounding_box=bounding_box,
                        confidence=cell.get("confidence", 0.0),
                    )
                )
            bounding_box = self._parse_bounding_box(table.get("boundingRegions", [{}])[0].get("polygon"))
            tables.append(
                DocumentTable(
                    rows=table.get("rowCount", 0),
                    cols=table.get("columnCount", 0),
                    cells=cells,
                    bounding_box=bounding_box,
                )
            )
        return tables

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