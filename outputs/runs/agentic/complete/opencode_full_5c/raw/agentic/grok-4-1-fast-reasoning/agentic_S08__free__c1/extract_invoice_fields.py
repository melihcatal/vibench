import os
from google.cloud import documentai_v1 as documentai
from document_models import InvoiceExtract, ExtractedField, LineItem, Confidence
from document_client import load_image_bytes, get_mime_type


def extract_invoice_fields(image_path: str) -> InvoiceExtract:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_INVOICE_PROCESSOR_ID")
    if not all([project_id, processor_id]):
        raise ValueError(
            "Missing Google Cloud env vars: GOOGLE_CLOUD_PROJECT_ID, GOOGLE_INVOICE_PROCESSOR_ID"
        )
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)
    image_bytes = load_image_bytes(image_path)
    mime_type = get_mime_type(image_path)
    document = documentai.RawDocument(content=image_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=document)
    result = client.process_request(request=request)
    document_object = result.document
    entity_dict = {}
    for entity in document_object.entities:
        entity_type = entity.type_.split("/")[-1]
        if entity_type not in entity_dict:
            entity_dict[entity_type] = []
        entity_dict[entity_type].append(
            {
                "content": entity.mention_text,
                "confidence": entity.confidence,
            }
        )
    vendor_data = entity_dict.get(
        "supplier_name", entity_dict.get("vendor_name", [{}])
    )[0]
    vendor = ExtractedField(
        content=vendor_data.get("content", ""),
        confidence=Confidence(value=vendor_data.get("confidence", 0.0)),
    )
    date_data = entity_dict.get("invoice_date", [{}])[0]
    invoice_date = ExtractedField(
        content=date_data.get("content", ""),
        confidence=Confidence(value=date_data.get("confidence", 0.0)),
    )
    total_data = entity_dict.get("total_amount", entity_dict.get("total", [{}]))[0]
    total_amount = ExtractedField(
        content=total_data.get("content", ""),
        confidence=Confidence(value=total_data.get("confidence", 0.0)),
    )
    line_items = []
    for page in document_object.pages:
        for table in getattr(page, "tables", []):
            for row in getattr(table, "body_rows", []):
                row_texts = []
                for cell in row.cells:
                    cell_text = ""
                    if (
                        hasattr(cell, "layout")
                        and hasattr(cell.layout, "text_anchor")
                        and cell.layout.text_anchor.content
                    ):
                        cell_text = "".join(
                            [t.content for t in cell.layout.text_anchor.content]
                        )
                    row_texts.append(cell_text)
                if len(row_texts) >= 2:
                    try:
                        price = float(row_texts[-1].replace("$", "").replace(",", ""))
                        line_items.append(
                            LineItem(
                                description=row_texts[0],
                                total_price=price,
                                confidence=Confidence(value=0.85),
                            )
                        )
                    except ValueError:
                        pass
    return InvoiceExtract(
        vendor=vendor,
        invoice_date=invoice_date,
        total_amount=total_amount,
        line_items=line_items[:10],
        raw_response={"entities": entity_dict},
    )
