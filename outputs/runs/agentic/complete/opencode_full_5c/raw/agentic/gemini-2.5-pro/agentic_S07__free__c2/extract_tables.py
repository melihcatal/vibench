from typing import List
from google.cloud import vision
from document_client import get_vision_client
from document_models import Table, TableRow, TableCell, BoundingBox


def get_text_from_symbols(symbols):
    return "".join([symbol.text for symbol in symbols])


def extract_tables_from_image(image_path: str) -> List[Table]:
    """
    Extracts tables from a document image using Google Cloud Vision API.
    """
    client = get_vision_client()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    tables = []
    for page in document.pages:
        for block in page.blocks:
            if block.block_type == vision.Block.BlockType.TABLE:
                for table in (
                    block.paragraphs
                ):  # In the API, tables are in paragraphs of table blocks
                    rows = []
                    for row in table.words:  # Rows are 'words' in this context
                        cells = []
                        for cell in row.symbols:  # Cells are 'symbols'
                            vertices = cell.bounding_box.vertices
                            bbox = BoundingBox(
                                x1=vertices[0].x,
                                y1=vertices[0].y,
                                x2=vertices[2].x,
                                y2=vertices[2].y,
                            )
                            cells.append(
                                TableCell(
                                    text=get_text_from_symbols(cell.symbols),
                                    bounding_box=bbox,
                                )
                            )
                        rows.append(TableRow(cells=cells))

                    vertices = table.bounding_box.vertices
                    table_bbox = BoundingBox(
                        x1=vertices[0].x,
                        y1=vertices[0].y,
                        x2=vertices[2].x,
                        y2=vertices[2].y,
                    )
                    tables.append(Table(rows=rows, bounding_box=table_bbox))
    return tables
