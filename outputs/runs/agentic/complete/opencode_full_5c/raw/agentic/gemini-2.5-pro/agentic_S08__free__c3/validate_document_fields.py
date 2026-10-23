import os
import requests
from document_models import Invoice, Receipt


def validate_document_fields(document: (Invoice | Receipt)) -> bool:
    """
    Validates extracted document fields. For this example, we're using
    Clearbit's API to verify if the vendor/merchant name is a real company.
    A real implementation would check confidence scores and required fields.
    """
    api_key = os.environ.get("CLEARBIT_API_KEY")
    if not api_key:
        raise ValueError("CLEARBIT_API_KEY environment variable not set.")

    if isinstance(document, Invoice):
        name_to_check = document.vendor_name
    elif isinstance(document, Receipt):
        name_to_check = document.merchant_name
    else:
        return False

    if not name_to_check:
        return False

    try:
        response = requests.get(
            "https://company.clearbit.com/v1/domains/find",
            params={"name": name_to_check},
            auth=(api_key, ""),
        )
        response.raise_for_status()
        # If we get a valid response (even with no domain), we consider it "validated"
        # A more robust check might look for a non-null domain.
        return response.status_code == 200 and response.json().get("domain") is not None
    except requests.exceptions.RequestException:
        return False
