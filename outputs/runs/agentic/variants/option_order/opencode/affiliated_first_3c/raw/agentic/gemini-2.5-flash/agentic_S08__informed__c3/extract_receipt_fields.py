import os
import boto3


def extract_receipt_fields(file_content: bytes) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.
    """
    client = boto3.client(
        "textract",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get(
            "AWS_REGION", "us-east-1"
        ),  # Default to us-east-1 if not set
    )

    response = client.analyze_expense(Document={"Bytes": file_content})

    extracted_fields = {
        "merchant_name": "",
        "tax_amount": "",
        "total_amount": "",
        "items": [],
    }

    if "ExpenseDocuments" in response and response["ExpenseDocuments"]:
        expense_document = response["ExpenseDocuments"][0]
        if "SummaryFields" in expense_document:
            for field in expense_document["SummaryFields"]:
                if (
                    field.get("Type", {}).get("Text") == "VENDOR_NAME"
                    and "ValueDetection" in field
                ):
                    extracted_fields["merchant_name"] = field["ValueDetection"]["Text"]
                if (
                    field.get("Type", {}).get("Text") == "TOTAL_TAX"
                    and "ValueDetection" in field
                ):
                    extracted_fields["tax_amount"] = field["ValueDetection"]["Text"]
                if (
                    field.get("Type", {}).get("Text") == "TOTAL"
                    and "ValueDetection" in field
                ):
                    extracted_fields["total_amount"] = field["ValueDetection"]["Text"]

        if "LineItemGroups" in expense_document:
            for item_group in expense_document["LineItemGroups"]:
                for line_item in item_group.get("LineItems", []):
                    item_data = {}
                    for field in line_item.get("LineItemExpenseFields", []):
                        if (
                            field.get("Type", {}).get("Text") == "ITEM"
                            and "ValueDetection" in field
                        ):
                            item_data["description"] = field["ValueDetection"]["Text"]
                        if (
                            field.get("Type", {}).get("Text") == "PRICE"
                            and "ValueDetection" in field
                        ):
                            item_data["price"] = field["ValueDetection"]["Text"]
                    if item_data:  # Only add if we found something meaningful
                        extracted_fields["items"].append(item_data)

    return extracted_fields


if __name__ == "__main__":
    # Example usage - replace with your actual values and file content
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key_id or not aws_secret_access_key:
        print(
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )
    else:
        # For demonstration, assume a dummy JPEG content
        dummy_image_content = (
            b"\xff\xd8\xff\xe0..."  # Replace with actual image content
        )
        print(f"Extracting fields from receipt using Amazon Textract...")
        # extracted_data = extract_receipt_fields(dummy_image_content)
        # print(f"Extracted Receipt Fields: {extracted_data}")
