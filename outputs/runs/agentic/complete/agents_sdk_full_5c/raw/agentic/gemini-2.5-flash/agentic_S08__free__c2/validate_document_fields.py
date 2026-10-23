import os
from typing import Dict, Any, List, Optional
from google.cloud import dlp_v2 as dlp
from document_client import DocumentClients, PROJECT_ID
from document_models import NormalizedExpense

# DLP Inspect Template ID (optional, but good practice for repeatable scans)
# INSPECT_TEMPLATE_NAME = os.environ.get("DLP_INSPECT_TEMPLATE_NAME", f"projects/{PROJECT_ID}/inspectTemplates/your-template-id")

def validate_document_fields(expense_record: NormalizedExpense) -> NormalizedExpense:
    """Validates required structured fields and checks for sensitive data using Google Cloud DLP.

    Args:
        expense_record: A NormalizedExpense dataclass instance.

    Returns:
        The NormalizedExpense instance with validation status updated.
    """
    dlp_client = DocumentClients.get_dlp_client()
    project_path = f"projects/{PROJECT_ID}"

    validation_results = {
        "required_fields_present": True,
        "sensitive_data_found": False,
        "sensitive_data_details": []
    }

    # --- 1. Basic Required Field Presence Validation ---
    required_fields = [
        expense_record.primary_vendor_merchant,
        expense_record.transaction_date,
        expense_record.total_expense_amount,
        expense_record.standardized_currency,
    ]

    if any(field is None for field in required_fields):
        validation_results["required_fields_present"] = False
        # Add more granular missing field details if needed

    # --- 2. Sensitive Data Detection using Google Cloud DLP ---
    # We'll check the primary vendor/merchant and any item descriptions/notes for sensitive info.
    text_to_inspect = []
    if expense_record.primary_vendor_merchant:
        text_to_inspect.append(expense_record.primary_vendor_merchant)
    if expense_record.notes:
        text_to_inspect.append(expense_record.notes)
    for item in expense_record.expense_items:
        if item.description:
            text_to_inspect.append(item.description)

    if text_to_inspect:
        # Create a list of content items to inspect
        items = [{'value': text} for text in text_to_inspect if text is not None]

        # Configure the inspect request
        inspect_config = dlp.InspectConfig(
            info_types=[
                {"name": "EMAIL_ADDRESS"},
                {"name": "PHONE_NUMBER"},
                {"name": "CREDIT_CARD_NUMBER"},
                {"name": "SSN"}, # For US Social Security Number
                {"name": "IBAN_CODE"},
            ],
            min_likelihood=dlp.Likelihood.POSSIBLE,
            include_quote=True,
        )

        try:
            response = dlp_client.inspect_content(
                request=dlp.InspectContentRequest(
                    parent=project_path,
                    inspect_config=inspect_config,
                    item=dlp.ContentItem(table=dlp.Table(rows=[dlp.Table.Row(values=[dlp.Table.Value(str_value=text) for text in text_to_inspect if text is not None]))) if text_to_inspect else None,
                )
            )

            # Simplified inspection for the example, a real implementation would iterate through findings
            # to pinpoint exact locations.
            if response.result.findings:
                validation_results["sensitive_data_found"] = True
                for finding in response.result.findings:
                    validation_results["sensitive_data_details"].append({
                        "info_type": finding.info_type.name,
                        "likelihood": dlp.Likelihood(finding.likelihood).name,
                        "quote": finding.quote
                    })

        except Exception as e:
            print(f"Error during DLP inspection: {e}")
            validation_results["dlp_error"] = str(e)

    expense_record.validation_status = validation_results
    return expense_record
