import google.cloud.documentai as documentai


def extract_receipt_fields(receipt_path):
    client = documentai.DocumentProcessorClient()
    with open(receipt_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(raw_document=raw_document)
    result = client.process_document(request=request)

    merchant = result.document.entities[0].mention_text
    tax = result.document.entities[1].mention_text
    total = result.document.entities[2].mention_text
    items = [entity.mention_text for entity in result.document.entities[3:]]

    return {"merchant": merchant, "tax": tax, "total": total, "items": items}
