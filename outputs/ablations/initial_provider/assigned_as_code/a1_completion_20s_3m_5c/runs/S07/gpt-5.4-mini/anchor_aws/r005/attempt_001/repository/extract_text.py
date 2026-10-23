import boto3


def extract_text(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.detect_document_text(Document={"Bytes": payload["document_bytes"]})
    return {"text": "\n".join(b["Text"] for b in response["Blocks"] if b["BlockType"] == "LINE")}
