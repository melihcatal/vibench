import os
import boto3


def extract_receipt_fields(file_bytes: bytes):
    """
    Extracts merchant, tax, total, and items from a receipt using Amazon Textract AnalyzeExpense.
    """
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY should be set in environment variables
    textract_client = boto3.client(
        "textract", region_name="us-east-1"
    )  # Specify your AWS region

    response = textract_client.analyze_expense(Document={"Bytes": file_bytes})

    extracted_data = {
        "merchant_name": None,
        "tax_amount": None,
        "total_amount": None,
        "line_items": [],
    }

    for expense_document in response["ExpenseDocuments"]:
        for field in expense_document["SummaryFields"]:
            if "Type" in field and "Text" in field["ValueDetection"]:
                if field["Type"]["Text"] == "VENDOR_NAME":
                    extracted_data["merchant_name"] = field["ValueDetection"]["Text"]
                elif field["Type"]["Text"] == "TOTAL_TAX":
                    extracted_data["tax_amount"] = field["ValueDetection"]["Text"]
                elif field["Type"]["Text"] == "TOTAL":
                    extracted_data["total_amount"] = field["ValueDetection"]["Text"]

        if "LineItemGroups" in expense_document:
            for item_group in expense_document["LineItemGroups"]:
                for line_item in item_group["LineItems"]:
                    item_details = {}
                    for field in line_item["LineItemExpenseFields"]:
                        if "Type" in field and "Text" in field["ValueDetection"]:
                            if field["Type"]["Text"] == "ITEM":
                                item_details["description"] = field["ValueDetection"][
                                    "Text"
                                ]
                            elif field["Type"]["Text"] == "PRICE":
                                item_details["price"] = field["ValueDetection"]["Text"]
                            elif field["Type"]["Text"] == "QUANTITY":
                                item_details["quantity"] = field["ValueDetection"][
                                    "Text"
                                ]
                    if item_details:
                        extracted_data["line_items"].append(item_details)

    return extracted_data


if __name__ == "__main__":
    # Placeholder for actual usage with AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY set
    if not os.environ.get("AWS_ACCESS_KEY_ID") or not os.environ.get(
        "AWS_SECRET_ACCESS_KEY"
    ):
        print(
            "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )
    else:
        # Example usage (replace with actual file content)
        sample_file_content = b"Your receipt content here"
        # extracted = extract_receipt_fields(sample_file_content)
        # print(extracted)
        print("Amazon Textract client configured for receipt extraction.")
