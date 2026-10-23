import boto3
import logging

logger = logging.getLogger(__name__)


def extract_invoice_fields(bucket_name: str, document_name: str) -> list:
    """
    Extracts structured expense data from a document in an S3 bucket
    using Amazon Textract's AnalyzeExpense API.

    Args:
        bucket_name (str): The name of the S3 bucket.
        document_name (str): The name of the document file in the S3 bucket.

    Returns:
        list: A list of dictionaries representing extracted summary fields.
    """
    textract_client = boto3.client("textract")

    try:
        response = textract_client.analyze_expense(
            Document={"S3Object": {"Bucket": bucket_name, "Name": document_name}}
        )

        extracted_fields = []
        for expense_doc in response.get("ExpenseDocuments", []):
            for summary_field in expense_doc.get("SummaryFields", []):
                field_info = {
                    "type": summary_field.get("Type", {}).get("Text"),
                    "label": summary_field.get("LabelDetection", {}).get("Text"),
                    "value": summary_field.get("ValueDetection", {}).get("Text"),
                    "confidence": summary_field.get("ValueDetection", {}).get(
                        "Confidence"
                    ),
                }
                extracted_fields.append(field_info)
        return extracted_fields

    except Exception as e:
        logger.error(f"Error during Textract AnalyzeExpense call: {e}")
        return []
