from document_client import textract_client


def extract_receipt_fields(document_bytes):
    client = textract_client()
    response = client.analyze_document(
        Document={"Bytes": document_bytes}, FeatureTypes=["FORMS", "TABLES"]
    )
    fields = {"merchant": None, "tax": None, "total": None, "items": []}
    for block in response.get("Blocks", []):
        text = block.get("Text", "")
        lower = text.lower()
        if "merchant" in lower:
            fields["merchant"] = text
        elif "tax" in lower:
            fields["tax"] = text
        elif "total" in lower:
            fields["total"] = text
        elif block.get("BlockType") == "LINE" and text:
            fields["items"].append(text)
    return fields
