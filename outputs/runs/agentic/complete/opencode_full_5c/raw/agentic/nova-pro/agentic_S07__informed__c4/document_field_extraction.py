from document_client import textract_client


def extract_structured_fields(document_path: str) -> Dict:
    with open(document_path, "rb") as document:
        response = textract_client.analyze_document(
            Document={"Bytes": document.read()}, FeatureTypes=["FORMS"]
        )
        fields = {
            item["KeyDetection"]["Text"]: item["ValueDetection"]["Text"]
            for item in response["Blocks"]
            if item["BlockType"] == "KEY_VALUE_SET"
        }
        return fields
