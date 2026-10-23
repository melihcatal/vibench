from openai import OpenAI
from document_client import get_openai_config
from document_models import InvoiceExtraction, ReceiptExtraction, DocumentField
from typing import Union, List

def validate_document_fields(extracted_data: Union[InvoiceExtraction, ReceiptExtraction], required_fields: List[str], min_confidence: float = 0.7) -> dict:
    config = get_openai_config()
    api_key = config.get('api_key')
    if not api_key:
        raise ValueError("OpenAI API key must be configured.")
    
    client = OpenAI(api_key=api_key)

    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "validation_notes": []
    }

    data_dict = extracted_data.__dict__

    # Check for required fields and confidence scores
    for field_name in required_fields:
        field_value = data_dict.get(field_name)
        if not field_value:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field_name)
        elif isinstance(field_value, DocumentField):
            if field_value.confidence is None or field_value.confidence < min_confidence:
                validation_results["is_valid"] = False
                validation_results["low_confidence_fields"].append({'field': field_name, 'confidence': field_value.confidence})
        elif isinstance(field_value, list): # Handle line items, assuming they are lists of LineItem objects or dicts
            if not field_value:
                validation_results["is_valid"] = False
                validation_results["missing_fields"].append(field_name)
            else:
                # For line items, check if at least one item exists, and optionally check sub-fields
                # This example does a basic check if the list is not empty.
                pass # More complex line item validation can be added here if needed.

    # Use OpenAI to provide general validation notes or identify potential issues beyond simple checks
    try:
        prompt = f"Review the following extracted document data and provide any observations on its completeness or potential inaccuracies, especially regarding missing or low-confidence fields. Focus on the overall quality for structured data extraction. Data: {json.dumps(data_dict)}"
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using a more recent model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that validates structured document extraction data."},
                {"role": "user", "content": prompt}
            ]
        )
        validation_results["validation_notes"].append(response.choices[0].message.content)
    except Exception as e:
        validation_results["validation_notes"].append(f"Error calling OpenAI for advanced validation: {e}")

    return validation_results
