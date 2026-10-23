import json
import os
from typing import Any, Dict, List, Optional

from google.cloud import documentai


def _env(name: str, required: bool = True) -> Optional[str]:
    value = os.getenv(name)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def extract_tables(document_path: str, project_id: Optional[str] = None, location: Optional[str] = None, processor_id: Optional[str] = None, mime_type: str = "application/pdf") -> Dict[str, Any]:
    project_id = project_id or _env("GOOGLE_CLOUD_PROJECT")
    location = location or _env("GOOGLE_CLOUD_LOCATION") or "us"
    processor_id = processor_id or _env("DOCUMENT_AI_PROCESSOR_ID")

    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)

    with open(document_path, "rb") as f:
        raw_document = documentai.RawDocument(content=f.read(), mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    extracted_tables: List[Dict[str, Any]] = []
    for page_index, page in enumerate(document.pages):
        for table_index, table in enumerate(page.tables):
            rows: List[List[str]] = []
            for row in table.header_rows + table.body_rows:
                cells: List[str] = []
                for cell in row.cells:
                    text = _text_from_anchor(document.text, cell.layout.text_anchor)
                    cells.append(text)
                rows.append(cells)

            extracted_tables.append(
                {
                    "page": page_index + 1,
                    "table_index": table_index,
                    "header_rows": len(table.header_rows),
                    "body_rows": len(table.body_rows),
                    "rows": rows,
                }
            )

    return {"tables": extracted_tables}


def _text_from_anchor(text: str, text_anchor: Any) -> str:
    if not text_anchor or not getattr(text_anchor, "text_segments", None):
        return ""
    parts: List[str] = []
    for segment in text_anchor.text_segments:
        start = int(segment.start_index) if segment.start_index else 0
        end = int(segment.end_index) if segment.end_index else len(text)
        parts.append(text[start:end])
    return "".join(parts).strip()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Extract tables from a document using Google Cloud Document AI")
    parser.add_argument("document_path")
    parser.add_argument("--project-id")
    parser.add_argument("--location")
    parser.add_argument("--processor-id")
    parser.add_argument("--mime-type", default="application/pdf")
    args = parser.parse_args()

    print(
        json.dumps(
            extract_tables(
                args.document_path,
                project_id=args.project_id,
                location=args.location,
                processor_id=args.processor_id,
                mime_type=args.mime_type,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
