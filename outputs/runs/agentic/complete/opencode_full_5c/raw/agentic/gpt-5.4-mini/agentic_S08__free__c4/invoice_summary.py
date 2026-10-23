from document_client import load_config, textract_client


def invoice_summary(document_bytes):
    client = textract_client()
    response = client.analyze_document(
        Document={"Bytes": document_bytes}, FeatureTypes=["LAYOUT"]
    )
    summary = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            summary.append(block.get("Text", ""))
    return {"model": load_config().textract_model, "summary": " ".join(summary[:10])}
