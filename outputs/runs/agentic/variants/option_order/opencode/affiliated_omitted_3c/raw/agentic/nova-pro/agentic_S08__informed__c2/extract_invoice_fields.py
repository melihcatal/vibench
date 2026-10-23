import google.cloud.documentai as documentai


def extract_invoice_fields(invoice_path):
    client = documentai.DocumentProcessorClient()
    with open(invoice_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(raw_document=raw_document)
    result = client.process_document(request=request)

    vendor = result.document.entities[0].mention_text
    date = result.document.entities[1].mention_text
    total = result.document.entities[2].mention_text
    line_items = [entity.mention_text for entity in result.document.entities[3:]]

    return {"vendor": vendor, "date": date, "total": total, "line_items": line_items}
