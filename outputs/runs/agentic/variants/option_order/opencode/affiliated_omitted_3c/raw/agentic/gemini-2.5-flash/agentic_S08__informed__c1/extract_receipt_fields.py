import os
import boto3


def extract_receipt_fields(document_bytes: bytes) -> dict:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    client = boto3.client(
        "textract",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    response = client.analyze_expense(Document={"Bytes": document_bytes})

    extracted_data = {}
    if response["ExpenseDocuments"]:
        expense_document = response["ExpenseDocuments"][0]
        if "SummaryFields" in expense_document:
            for field in expense_document["SummaryFields"]:
                if (
                    field["Type"]["Text"] == "MERCHANT_NAME"
                    and "ValueDetection" in field
                ):
                    extracted_data["merchant_name"] = field["ValueDetection"]["Text"]
                elif field["Type"]["Text"] == "TOTAL" and "ValueDetection" in field:
                    extracted_data["total"] = float(field["ValueDetection"]["Text"])
                elif field["Type"]["Text"] == "TAX" and "ValueDetection" in field:
                    extracted_data["tax"] = float(field["ValueDetection"]["Text"])

        if "LineItemGroups" in expense_document:
            extracted_data["items"] = []
            for group in expense_document["LineItemGroups"]:
                for item in group["LineItems"]:
                    line_item = {}
                    for field in item["LineItemExpenseFields"]:
                        if (
                            field["Type"]["Text"] == "ITEM"
                            and "ValueDetection" in field
                        ):
                            line_item["description"] = field["ValueDetection"]["Text"]
                        elif (
                            field["Type"]["Text"] == "PRICE"
                            and "ValueDetection" in field
                        ):
                            line_item["amount"] = float(field["ValueDetection"]["Text"])
                    if line_item:
                        extracted_data["items"].append(line_item)

    return extracted_data
