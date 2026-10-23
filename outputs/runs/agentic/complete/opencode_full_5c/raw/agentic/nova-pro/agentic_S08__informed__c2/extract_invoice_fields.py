from google.cloud import documentai


def extract_invoice_fields(invoice_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(invoice_path, "rb") as image:
        image_content = image.read()
    document = {"content": image_content, "mime_type": "application/pdf"}
    response = client.process_document(
        name="projects/project-id/locations/location-id/processors/processor-id",
        document=document,
    )
    vendor = response.document.fields["vendor"].string_value
    date = response.document.fields["date"].string_value
    total = response.document.fields["total"].string_value
    line_items = [
        item.text for item in response.document.fields["line_items"].list_value.values
    ]
    return {"vendor": vendor, "date": date, "total": total, "line_items": line_items}
