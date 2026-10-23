import pandas as pd
import json


def extract_tables(document):
    """Extract table cells and row structure from a Google Document AI response."""
    tables = []
    for entity in document.entities:
        if entity.type_ == "TABLE":
            table = {"headers": [], "rows": []}
            for row in entity.pages[0].layout.pages[0].tables:
                for cell in row.cells:
                    table["rows"].append(
                        [cell.text if cell.text else "" for _ in cell.detected_breaks]
                    )
            tables.append(table)
    return tables
