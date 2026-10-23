from document_client import load_document_input, s3_object_reference, textract_client
from document_models import TextExtractionResult


def extract_text(bucket: str | None = None, key: str | None = None, version: str | None = None) -> TextExtractionResult:
    bucket, key, version = load_document_input(bucket, key, version)
    response = textract_client().detect_document_text(Document=s3_object_reference(bucket, key, version))
    lines = [b.get("Text", "") for b in response.get("Blocks", []) if b.get("BlockType") == "LINE"]
    return TextExtractionResult(text="\n".join(lines), lines=lines, pages=[], raw=response)


def main():
    return extract_text()
