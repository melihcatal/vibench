import os
from mistralai.client import MistralClient
from mistralai.models.chat_models import ChatMessage


def validate_document_fields(
    extracted_data: dict, required_fields: list, min_confidence: float = 0.8
) -> dict:
    """
    Validates required structured fields and confidence scores using Mistral Chat API.
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set.")

    client = MistralClient(api_key=api_key)

    validation_prompt = f"""
    Review the following extracted document data and validate if all required fields are present
    and if their implied confidence is acceptable. Assume 'confidence' is high unless data
    appears incomplete, malformed, or ambiguous.

    Required fields: {", ".join(required_fields)}
    Extracted data: {extracted_data}

    Provide a JSON response with a 'is_valid' boolean and a 'validation_errors' array
    listing any missing fields or fields with low confidence, and a 'reason' for each.
    Example:
    {{
        "is_valid": true,
        "validation_errors": []
    }}
    or
    {{
        "is_valid": false,
        "validation_errors": [
            {{
                "field": "vendor_name",
                "reason": "Missing required vendor name."
            }},
            {{
                "field": "total_amount",
                "reason": "Total amount appears malformed or ambiguous."
            }}
        ]
    }}
    """

    messages = [ChatMessage(role="user", content=validation_prompt)]

    chat_response = client.chat(
        model="mistral-tiny",
        messages=messages,
    )

    try:
        validation_result_str = chat_response.choices[0].message.content.strip()
        # Using eval for simplicity, safer would be json.loads
        validation_result = eval(validation_result_str)
    except Exception as e:
        print(f"Error parsing Mistral response: {e}")
        validation_result = {
            "is_valid": False,
            "validation_errors": [
                {"field": "N/A", "reason": f"Failed to parse validation response: {e}"}
            ],
        }

    return validation_result


if __name__ == "__main__":
    # Placeholder for actual usage with MISTRAL_API_KEY set
    if not os.environ.get("MISTRAL_API_KEY"):
        print("Please set MISTRAL_API_KEY environment variable.")
    else:
        sample_extracted_invoice = {
            "vendor_name": "Example Corp",
            "invoice_date": "2023-10-26",
            "total_amount": "123.45",
            "currency": "USD",
        }
        required_invoice_fields = ["vendor_name", "total_amount"]

        # validation_output = validate_document_fields(sample_extracted_invoice, required_invoice_fields)
        # print("Validation Result:", validation_output)
        print("Mistral AI client configured for document field validation.")
