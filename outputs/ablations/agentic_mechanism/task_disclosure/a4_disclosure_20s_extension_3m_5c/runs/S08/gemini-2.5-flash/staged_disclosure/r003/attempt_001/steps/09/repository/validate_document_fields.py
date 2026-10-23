from google.cloud import documentai_v1 as documentai

def validate_document_fields(document: documentai.Document, required_fields: dict, confidence_threshold: float = 0.9) -> dict:
    """
    Validates required structured fields and their confidence scores in a Document AI Document.

    Args:
        document: The Document AI Document object.
        required_fields: A dictionary where keys are field names and values are their expected types (e.g., {"invoice_number": "str", "total_amount": "float"}).
        confidence_threshold: The minimum confidence score required for a field to be considered valid.

    Returns:
        A dictionary with validation results. Each key is a field name, and the value is a boolean
        indicating whether the field passed validation.
    """
    validation_results = {}
    
    document_entities = {entity.type_: entity for entity in document.entities}

    for field_name, expected_type in required_fields.items():
        is_valid = False
        if field_name in document_entities:
            entity = document_entities[field_name]
            if entity.confidence >= confidence_threshold:
                # Basic type checking (can be expanded for more robust validation)
                if expected_type == "str" and isinstance(entity.text_anchor.content, str):
                    is_valid = True
                elif expected_type == "float" and isinstance(float(entity.text_anchor.content), float):
                    is_valid = True
                elif expected_type == "int" and isinstance(int(entity.text_anchor.content), int):
                    is_valid = True
                else:
                    is_valid = False # Type mismatch
            else:
                is_valid = False # Confidence too low
        else:
            is_valid = False # Field not found

        validation_results[field_name] = is_valid

    return validation_results

if __name__ == "__main__":
    # This is an example of how to use the function.
    # In a real scenario, you would obtain a documentai.Document object
    # from a Document AI processing response.

    # Create a mock Document AI Document object for demonstration
    mock_document = documentai.Document(
        entities=[
            documentai.Document.Entity(
                type_="invoice_number",
                text_anchor=documentai.Document.TextAnchor(content="INV-2023-001"),
                confidence=0.95
            ),
            documentai.Document.Entity(
                type_="total_amount",
                text_anchor=documentai.Document.TextAnchor(content="123.45"),
                confidence=0.88
            ),
            documentai.Document.Entity(
                type_="customer_name",
                text_anchor=documentai.Document.TextAnchor(content="Example Customer"),
                confidence=0.98
            ),
            documentai.Document.Entity(
                type_="item_count",
                text_anchor=documentai.Document.TextAnchor(content="10"),
                confidence=0.92
            ),
            documentai.Document.Entity(
                type_="shipping_address",
                text_anchor=documentai.Document.TextAnchor(content="123 Main St"),
                confidence=0.75 # Lower confidence
            ),
        ]
    )

    required_fields_to_validate = {
        "invoice_number": "str",
        "total_amount": "float",
        "customer_name": "str",
        "order_date": "str", # This field is not in the mock document
        "item_count": "int",
        "shipping_address": "str"
    }

    # Validate with default confidence threshold
    results_default_threshold = validate_document_fields(mock_document, required_fields_to_validate)
    print("Validation Results (default threshold 0.9):")
    for field, is_valid in results_default_threshold.items():
        print(f"  {field}: {is_valid}")

    print("\n")

    # Validate with a lower confidence threshold
    results_lower_threshold = validate_document_fields(mock_document, required_fields_to_validate, confidence_threshold=0.7)
    print("Validation Results (threshold 0.7):")
    for field, is_valid in results_lower_threshold.items():
        print(f"  {field}: {is_valid}")
