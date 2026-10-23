import boto3
from typing import List, Dict, Any
from document_client import DocumentClient
from document_models import DocumentPayload, TableExtractionResult, Table, TableCell

def extract_tables(payload: DocumentPayload, config: Dict[str, Any] = None) -> TableExtractionResult:
    config = config or {}
    client = DocumentClient(config).get_textract_client()

    response = client.analyze_document(
        Document={"Bytes": payload.document_bytes},
        FeatureTypes=["TABLES"]
    )

    tables: List[Table] = []
    blocks_by_id = {block["Id"]: block for block in response.get("Blocks", [])}

    for block in response.get("Blocks", []):
        if block["BlockType"] == "TABLE":
            table_cells: List[List[TableCell]] = []
            # Initialize rows based on max row index found in cells
            max_row_index = 0
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        cell_block = blocks_by_id.get(child_id)
                        if cell_block and cell_block["BlockType"] == "CELL":
                            r_index = cell_block["RowIndex"]
                            if r_index > max_row_index:
                                max_row_index = r_index
            
            for _ in range(max_row_index):
                table_cells.append([])

            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        cell_block = blocks_by_id.get(child_id)
                        if cell_block and cell_block["BlockType"] == "CELL":
                            cell_content = ""
                            for cell_rel in cell_block.get("Relationships", []):
                                if cell_rel["Type"] == "CHILD":
                                    for word_id in cell_rel["Ids"]:
                                        word_block = blocks_by_id.get(word_id)
                                        if word_block and word_block["BlockType"] == "WORD":
                                            cell_content += word_block.get("Text", "") + " "
                            cell_content = cell_content.strip()
                            
                            row_idx = cell_block["RowIndex"] - 1 # 0-indexed
                            col_idx = cell_block["ColumnIndex"] - 1 # 0-indexed

                            # Ensure row exists
                            while len(table_cells) <= row_idx:
                                table_cells.append([])
                            # Ensure column exists for the row
                            while len(table_cells[row_idx]) <= col_idx:
                                table_cells[row_idx].append(None) # Placeholder

                            table_cells[row_idx][col_idx] = TableCell(
                                row_index=row_idx,
                                column_index=col_idx,
                                content=cell_content,
                                geometry=cell_block.get("Geometry", {})
                            )
            
            # Replace None placeholders with empty TableCell objects if needed, or filter them out
            # For simplicity, let's ensure all cells are present with empty strings if no content was found.
            # This can be refined based on exact rendering needs.
            final_rows = []
            for row in table_cells:
                current_row = []
                for cell_obj in row:
                    if cell_obj is None:
                        # Create a dummy cell if no content was found for this position
                        current_row.append(TableCell(row_index=0, column_index=0, content="", geometry={})) 
                    else:
                        current_row.append(cell_obj)
                final_rows.append(current_row)

            tables.append(Table(rows=final_rows, geometry=block.get("Geometry", {})))

    return TableExtractionResult(tables=tables)
