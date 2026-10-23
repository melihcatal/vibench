import os
import requests
import json


def validate_document_fields(document_fields: dict) -> dict:
    """
    Validates required structured fields and confidence scores using Azure AI Content Safety
    for content moderation of text fields.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        print("Azure Content Safety endpoint and key not configured.")
        return {
            "validation_status": "skipped",
            "issues": ["Azure Content Safety not configured"],
        }

    validation_results = {"validation_status": "success", "issues": []}
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    # Example: Check vendor name for content safety issues
    vendor_name = document_fields.get("vendor", {}).get("name")
    if vendor_name:
        text_to_analyze = {"text": vendor_name}
        try:
            response = requests.post(
                f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview",
                headers=headers,
                json=text_to_analyze,
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            analysis_result = response.json()

            # Example of checking for safety violations
            if analysis_result and "categoriesAnalysis" in analysis_result:
                for category_analysis in analysis_result["categoriesAnalysis"]:
                    if category_analysis["severity"] > 0:
                        validation_results["validation_status"] = "failed"
                        validation_results["issues"].append(
                            f"Vendor name '{vendor_name}' flagged for {category_analysis['category']} with severity {category_analysis['severity']}"
                        )
        except requests.exceptions.RequestException as e:
            validation_results["validation_status"] = "error"
            validation_results["issues"].append(
                f"Azure Content Safety API error for vendor name: {e}"
            )

    # Add checks for required fields and confidence scores (simplified for this example)
    required_fields = [("vendor", "name"), ("total_amount", "value"), ("date", None)]
    for field_path, sub_field in required_fields:
        current_field = document_fields.get(field_path)
        if current_field is None:
            validation_results["validation_status"] = "failed"
            validation_results["issues"].append(f"Missing required field: {field_path}")
        elif sub_field and current_field.get(sub_field) is None:
            validation_results["validation_status"] = "failed"
            validation_results["issues"].append(
                f"Missing required sub-field: {field_path}.{sub_field}"
            )

    return validation_results


if __name__ == "__main__":
    # Example usage - replace with actual data
    azure_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    azure_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not azure_endpoint or not azure_key:
        print(
            "Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )
    else:
        dummy_document_fields = {
            "transaction_type": "expense",
            "vendor": {"name": "Test Company", "address": "123 Main St"},
            "date": "2023-01-01",
            "total_amount": {"value": 100.00, "currency": "USD"},
            "tax_amount": {"value": 5.00, "currency": "USD"},
            "line_items": [
                {
                    "description": "Item 1",
                    "quantity": 1,
                    "unit_price": 95.00,
                    "total": 95.00,
                },
                {
                    "description": "Tax",
                    "quantity": 1,
                    "unit_price": 5.00,
                    "total": 5.00,
                },
            ],
            "document_type": "invoice",
        }
        print(f"Validating document fields using Azure AI Content Safety...")
        # validation_output = validate_document_fields(dummy_document_fields)
        # print(f"Validation Results: {json.dumps(validation_output, indent=2)}")
