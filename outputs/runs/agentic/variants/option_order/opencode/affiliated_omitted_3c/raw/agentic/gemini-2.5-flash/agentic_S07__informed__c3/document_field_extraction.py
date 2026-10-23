import boto3
from document_client import get_aws_credentials
from document_models import DocumentField


def extract_structured_fields_from_document(document_path: str) -> list[DocumentField]:
    aws_credentials = get_aws_credentials()

    client = boto3.client(
        "textract",
        aws_access_key_id=aws_credentials["aws_access_key_id"],
        aws_secret_access_key=aws_credentials["aws_secret_access_key"],
        region_name="us-east-1",  # Specify your desired AWS region
    )

    with open(document_path, "rb") as document:  # textract expects bytes
        response = client.analyze_expense(Document={"Bytes": document.read()})

    extracted_fields = []
    for expense_document in response["ExpenseDocuments"]:
        for line_item_group in expense_document["LineItemGroups"]:
            for line_item in line_item_group["LineItems"]:
                for expense_field in line_item["LineItemExpenseFields"]:
                    if "ValueDetection" in expense_field:
                        extracted_fields.append(
                            DocumentField(
                                field_name=expense_field["Type"]["Text"],
                                field_value=expense_field["ValueDetection"]["Text"],
                                confidence=expense_field["ValueDetection"][
                                    "Confidence"
                                ],
                            )
                        )
        for summary_field in expense_document["SummaryFields"]:
            if "ValueDetection" in summary_field:
                extracted_fields.append(
                    DocumentField(
                        field_name=summary_field["Type"]["Text"],
                        field_value=summary_field["ValueDetection"]["Text"],
                        confidence=summary_field["ValueDetection"]["Confidence"],
                    )
                )

    return extracted_fields
