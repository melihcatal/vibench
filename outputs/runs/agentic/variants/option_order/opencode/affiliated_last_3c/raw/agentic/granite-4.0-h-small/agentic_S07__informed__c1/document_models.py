from typing import Any, Dict, List, Union

# Local models for OCR/layout requests/response normalization


# Request structures
class OCRRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes


class LayoutRequest:
    def __init__(self, image_bytes: bytes, feature_types: List[str] = None):
        self.image_bytes = image_bytes
        self.feature_types = feature_types or ["FORMS"]


class TableExtractionRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes


class KVExtractionRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes


class ProviderResponse:
    """Normalized wrapper for responses from any OCR/layout provider."""

    def __init__(self, raw: Any):
        self.raw = raw

    def get_text(self) -> str:
        """Return plain text if available."""
        try:
            return " ".join(
                item["Text"]
                for item in self.raw["Blocks"]
                if item.get("BlockType") == "LINE"
            )
        except Exception:
            return ""

    def get_layout(self) -> Dict[str, Any]:
        """Return layout hierarchy."""
        layout = {"lines": [], "tables": [], "other": []}
        for item in self.raw.get("Blocks", []):
            t = item.get("BlockType")
            if t == "LINE":
                layout["lines"].append(item.get("Text"))
            elif t == "TABLE":
                layout["tables"].append(item)
            else:
                layout["other"].append(item)
        return layout

    def get_tables(self) -> List[List[str]]:
        """Return list of tables (each table is list of rows, each row list of cell values)."""
        tables = []
        for tbl in self.raw.get("Blocks", []):
            if tbl.get("BlockType") != "TABLE":
                continue
            rows = []
            for cell in tbl.get("Relationships", []):
                if cell.get("Type") != "CHILD":
                    continue
                cells = []
                for fid in cell.get("Ids", []):
                    cell_blk = next(
                        (b for b in self.raw["Blocks"] if b["Id"] == fid), None
                    )
                    if cell_blk and cell_blk.get("BlockType") == "CELL":
                        text = next(
                            (
                                b["Text"]
                                for b in self.raw["Blocks"]
                                if b["Id"]
                                == cell_blk.get("Relationships", [{}])[0].get(
                                    "Ids", [{}]
                                )[0]
                            ),
                            "",
                        )
                        cells.append(text)
            tables.append(cells)
        return tables

    def get_key_values(self) -> Dict[str, str]:
        """Return key/value pairs."""
        kv = {}
        for item in self.raw.get("Blocks", []):
            if item.get("BlockType") != "KEY_VALUE_SET":
                continue
            rel = item.get("Relationships", [])
            key = next((b.get("Text") for b in rel if b.get("Type") == "KEY"), "")
            value = next((b.get("Text") for b in rel if b.get("Type") == "VALUE"), "")
            if key and value:
                kv[key] = value
        return kv
