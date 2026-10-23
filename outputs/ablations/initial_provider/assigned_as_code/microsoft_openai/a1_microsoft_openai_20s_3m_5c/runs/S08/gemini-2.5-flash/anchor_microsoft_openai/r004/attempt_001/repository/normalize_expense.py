import requests
import json
from document_client import get_google_cloud_function_normalization_config
from document_models import NormalizedExpense

def normalize_expense(extracted_data: dict, document_type: str) -> NormalizedExpense:
    config = get_google_cloud_function_normalization_config()
    endpoint = config.get('endpoint')
    if not endpoint:
        raise ValueError("Google Cloud Function normalization endpoint must be configured.")

    # In a real scenario, this would call a Google Cloud Function that contains the normalization logic.
    # For this exercise, we simulate the call and return a simplified normalized structure.
    payload = {
        "extracted_data": extracted_data,
        "document_type": document_type
    }

    try:
        # Simulate a call to a Google Cloud Function for normalization
        # The actual function would parse extracted_data based on document_type
        # and return a NormalizedExpense structure.
        response = requests.post(endpoint, json=payload, timeout=5) # 5 second timeout
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        normalized_data = response.json()
        
        # Assuming the cloud function returns a dict compatible with NormalizedExpense
        return NormalizedExpense(**normalized_data)

    except requests.exceptions.RequestException as e:
        print(f"Error calling Google Cloud Function for normalization: {e}")
        # Fallback or error handling: return a partially normalized expense or raise
        # For now, we will construct a basic one without external call success.
        return NormalizedExpense(
            document_type=document_type,
            vendor_name=extracted_data.get('vendor', extracted_data.get('merchant')),
            transaction_date=extracted_data.get('date'),
            total_amount=float(extracted_data.get('total', 0)) if extracted_data.get('total') else 0.0,
            currency="USD", # Defaulting for simulation
            line_items=[],
            raw_extraction_data=extracted_data
        )

