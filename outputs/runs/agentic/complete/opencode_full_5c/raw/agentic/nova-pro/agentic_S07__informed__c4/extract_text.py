from document_client import textract_client


def extract_text(document_path: str) -> str:
    with open(document_path, "rb") as document:
        response = textract_client.detect_document_text(
            Document={"Bytes": document.read()}
        )
        text = " ".join(
            [item["Text"] for item in response["Blocks"] if item["BlockType"] == "WORD"]
        )
        return text
