import os
from google.cloud import documentai_v1 as documentai
from document_models import RawInvoice, LineItem


def extract_invoice_fields(document_path: str) -> RawInvoice:
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    location = "us"
    processor_id = "86e3482189466a6d"
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    client = documentai.DocumentProcessorServiceClient()

    with open(document_path, "rb") as file:
        content = file.read()

    raw_document = documentai.RawDocument(content=content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_request(request)
    document = result.document

    entities_dict = {}
    for entity in document.entities:
        entities_dict.setdefault(entity.type_, []).append(entity.mention_text)

    vendor = entities_dict.get("vendor_name", [""])[0]
    date = entities_dict.get("invoice_date", [""])[0]
    total = float(entities_dict.get("total_amount_incl_tax", ["0"])[0] or 0)

    line_items = []
    for page in document.pages:
        for table in getattr(page, "tables", []):
            for row in table.body_rows:
                cells = [cell.layout.text_anchor.content for cell in row.cells]
                if len(cells) >= 4:
                    line_items.append(
                        LineItem(
                            description=cells[0],
                            quantity=float(cells[1] or 0),
                            unit_price=float(cells[2] or 0),
                            total=float(cells[3] or 0),
                        )
                    )

    return RawInvoice(vendor=vendor, date=date, total=total, line_items=line_items)
