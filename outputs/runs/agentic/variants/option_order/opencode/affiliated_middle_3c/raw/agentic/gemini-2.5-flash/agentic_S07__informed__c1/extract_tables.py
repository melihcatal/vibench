import boto3
from document_client import AmazonTextractClient
from document_models import Table, TableCell
from typing import List


def extract_tables_from_textract(file_content: bytes) -> List[Table]:
    client = AmazonTextractClient().client

    response = client.analyze_document(
        Document={"Bytes": file_content}, FeatureTypes=["TABLES"]
    )

    tables: List[Table] = []
    for page in response["Pages"]:
        for block in page["Blocks"]:
            if block["BlockType"] == "TABLE":
                cells: List[TableCell] = []
                rows = 0
                cols = 0
                for relationship in block["Relationships"]:
                    if relationship["Type"] == "CHILD":
                        for child_id in relationship["Ids"]:
                            child_block = next(
                                (
                                    b
                                    for b in page["Blocks"]
                                    if b["Id"] == child_id and b["BlockType"] == "CELL"
                                ),
                                None,
                            )
                            if child_block:
                                content = ""
                                for cell_relationship in child_block["Relationships"]:
                                    if cell_relationship["Type"] == "CHILD":
                                        for text_id in cell_relationship["Ids"]:
                                            text_block = next(
                                                (
                                                    b
                                                    for b in page["Blocks"]
                                                    if b["Id"] == text_id
                                                    and b["BlockType"] == "WORD"
                                                ),
                                                None,
                                            )
                                            if text_block:
                                                content += text_block["Text"] + " "
                                cells.append(
                                    TableCell(
                                        content=content.strip(),
                                        row_index=child_block["RowIndex"],
                                        column_index=child_block["ColumnIndex"],
                                        row_span=child_block.get("RowSpan", 1),
                                        column_span=child_block.get("ColumnSpan", 1),
                                    )
                                )
                                rows = max(rows, child_block["RowIndex"])
                                cols = max(cols, child_block["ColumnIndex"])
                tables.append(Table(cells=cells, rows=rows, columns=cols))
    return tables
