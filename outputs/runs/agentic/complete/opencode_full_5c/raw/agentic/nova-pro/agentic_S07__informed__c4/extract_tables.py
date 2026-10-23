from document_client import textract_client


def extract_tables(document_path: str) -> List[Dict]:
    with open(document_path, "rb") as document:
        response = textract_client.analyze_document(
            Document={"Bytes": document.read()}, FeatureTypes=["TABLES"]
        )
        tables = [item for item in response["Blocks"] if item["BlockType"] == "TABLE"]
        return tables
