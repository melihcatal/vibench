from google.cloud import documentai


def extract_receipt_fields(file_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = {"content": image_content, "mime_type": "application/pdf"}
    document = client.process_document(raw_document=raw_document)

    extracted_data = {}
    for entity in document.entities:
        if entity.type_ == "MERCHANT":
            extracted_data["merchant"] = entity.mention_text
        elif entity.type_ == "TAX":
            extracted_data["tax"] = entity.mention_text
        elif entity.type_ == "TOTAL":
            extracted_data["total"] = entity.mention_text
        elif entity.type_ == "ITEMS":
            if "items" not in extracted_data:
                extracted_data["items"] = []
            extracted_data["items"].append(entity.mention_text)
    return extracted_data
