import boto3


def extract_tables(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(
        Document={"Bytes": payload["document_bytes"]}, Features=["TABLES"]
    )

    tables = []
    for block in response["Blocks"]:
        if block["BlockType"] == "TABLE":
            table_cells = []
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        cell_block = next(
                            (b for b in response["Blocks"] if b["Id"] == child_id), None
                        )
                        if cell_block and cell_block["BlockType"] == "CELL":
                            table_cells.append(
                                {
                                    "text": next(
                                        (
                                            t["Text"]
                                            for t in response["Blocks"]
                                            if t["Id"] == cell_block["Id"]
                                        ),
                                        "",
                                    ),
                                    "row_index": cell_block["RowIndex"],
                                    "column_index": cell_block["ColumnIndex"],
                                    "row_span": cell_block["RowSpan"],
                                    "column_span": cell_block["ColumnSpan"],
                                }
                            )
            tables.append({"id": block["Id"], "cells": table_cells})
    return {"tables": tables}
