from google.cloud import documentai


def extract_receipt_fields(project_id, location, processor_id, file_path):
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    merchant = result.document.fields["merchant"].string_value
    tax = result.document.fields["tax"].string_value
    total = result.document.fields["total"].string_value
    items = [item.text for item in result.document.entities if item.type_ == "ITEM"]

    return {"merchant": merchant, "tax": tax, "total": total, "items": items}
