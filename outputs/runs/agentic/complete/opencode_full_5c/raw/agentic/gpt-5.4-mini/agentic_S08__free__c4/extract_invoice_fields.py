from document_client import textract_client


def extract_invoice_fields(document_bytes):
    client = textract_client()
    response = client.analyze_document(
        Document={"Bytes": document_bytes}, FeatureTypes=["FORMS", "TABLES"]
    )
    fields = {"vendor": None, "date": None, "total": None, "line_items": []}
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "KEY_VALUE_SET":
            text = block.get("Text", "")
            lower = text.lower()
            if "vendor" in lower:
                fields["vendor"] = text
            elif "date" in lower:
                fields["date"] = text
            elif "total" in lower:
                fields["total"] = text
        if block.get("BlockType") == "LINE" and "item" in block.get("Text", "").lower():
            fields["line_items"].append(block.get("Text"))
    return fields
