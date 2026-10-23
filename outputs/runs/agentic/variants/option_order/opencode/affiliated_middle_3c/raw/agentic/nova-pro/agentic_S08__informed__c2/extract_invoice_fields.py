from google.cloud import documentai


def extract_invoice_fields(file_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = {"content": image_content, "mime_type": "application/pdf"}
    document = client.process_document(raw_document=raw_document)

    extracted_data = {}
    for entity in document.entities:
        if entity.type_ == "VENDOR":
            extracted_data["vendor"] = entity.mention_text
        elif entity.type_ == "DATE":
            extracted_data["date"] = entity.mention_text
        elif entity.type_ == "TOTAL":
            extracted_data["total"] = entity.mention_text
        elif entity.type_ == "LINE_ITEM":
            if "line_items" not in extracted_data:
                extracted_data["line_items"] = []
            extracted_data["line_items"].append(entity.mention_text)
    return extracted_data
