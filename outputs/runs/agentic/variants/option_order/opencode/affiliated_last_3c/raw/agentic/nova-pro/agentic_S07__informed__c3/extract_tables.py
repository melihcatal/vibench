import boto3

# Initialize the client
textract = boto3.client("textract")


def extract_tables(document_path):
    with open(document_path, "rb") as document_file:
        response = textract.analyze_document(
            Document={"Bytes": document_file.read()}, FeatureTypes=["TABLES"]
        )
        return response["Blocks"]
