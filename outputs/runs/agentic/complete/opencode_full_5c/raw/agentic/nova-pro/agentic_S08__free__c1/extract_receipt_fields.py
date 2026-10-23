import boto3
from document_models import NormalizationHelper


def extract_receipt_fields(document_path):
    textract_client = boto3.client("textract")
    with open(document_path, "rb") as document:
        response = textract_client.analyze_document(
            Document={"Bytes": document.read()}, FeatureTypes=["FORMS"]
        )
    extracted_data = NormalizationHelper.normalize_receipt_fields(response)
    return extracted_data
