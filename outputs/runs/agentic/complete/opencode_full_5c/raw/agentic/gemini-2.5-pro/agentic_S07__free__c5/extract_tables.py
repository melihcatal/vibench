from azure.ai.formrecognizer import DocumentAnalysisClient
from document_client import get_form_recognizer_client
from document_models import ExtractedTables, Table, TableCell, BoundingBox, Point


def extract_tables_from_document(document_path: str) -> ExtractedTables:
    document_analysis_client = get_form_recognizer_client()

    with open(document_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-layout", document=f
        )
    result = poller.result()

    tables = []
    for table_idx, table in enumerate(result.tables):
        cells = []
        for cell in table.cells:
            points = [Point(x=p.x, y=p.y) for p in cell.bounding_regions[0].polygon]
            cells.append(
                TableCell(
                    text=cell.content,
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                    bounding_box=BoundingBox(points=points),
                )
            )

        table_bounding_regions = table.bounding_regions[0]
        table_points = [Point(x=p.x, y=p.y) for p in table_bounding_regions.polygon]

        tables.append(
            Table(
                cells=cells,
                row_count=table.row_count,
                column_count=table.column_count,
                bounding_box=BoundingBox(points=table_points),
            )
        )

    return ExtractedTables(tables=tables)
