from document_models import (
    InvoiceFields,
    LineItem,
    ExtractionRequest,
    ExtractionResponse,
    invoice_to_dict,
)
from document_client import (
    load_mindee_config,
    parse_invoice_response,
    MINDEE_INVOICE_PRODUCT,
    extract_from_file_path,
    extract_from_bytes,
)

PROVIDER = "mindee"
PRODUCT = MINDEE_INVOICE_PRODUCT


def extract_invoice_fields(request: ExtractionRequest) -> ExtractionResponse:
    try:
        config = load_mindee_config()
        client = config.get_client()

        if request.document_bytes:
            mindee_response = extract_from_bytes(
                client, PRODUCT, request.document_bytes
            )
        elif request.document_path:
            mindee_response = extract_from_file_path(
                client, PRODUCT, request.document_path
            )
        else:
            return ExtractionResponse(
                success=False,
                error="No document provided",
                provider=PROVIDER,
            )

        parsed = parse_invoice_response(mindee_response)

        line_items = []
        for item_data in parsed.get("line_items", []):
            line_items.append(
                LineItem(
                    description=item_data.get("description", ""),
                    quantity=item_data.get("quantity", 0.0),
                    unit_price=item_data.get("unit_price", 0.0),
                    total_price=item_data.get("total_price", 0.0),
                    confidence=parsed.get("field_confidences", {}).get(
                        "line_items", 0.0
                    ),
                )
            )

        fields = InvoiceFields(
            vendor_name=parsed.get("vendor_name", ""),
            vendor_address=parsed.get("vendor_address", ""),
            invoice_number=parsed.get("invoice_number", ""),
            invoice_date=parsed.get("invoice_date", ""),
            due_date=parsed.get("due_date", ""),
            subtotal=parsed.get("subtotal", 0.0),
            tax=parsed.get("tax", 0.0),
            total=parsed.get("total", 0.0),
            currency=parsed.get("currency", "USD"),
            line_items=line_items,
            notes=parsed.get("notes", ""),
            raw_confidence=parsed.get("raw_confidence", 0.0),
            field_confidences=parsed.get("field_confidences", {}),
        )

        return ExtractionResponse(
            success=True,
            fields=fields,
            provider=PROVIDER,
            raw_response=invoice_to_dict(fields),
        )

    except Exception as e:
        return ExtractionResponse(
            success=False,
            error=str(e),
            provider=PROVIDER,
        )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        req = ExtractionRequest(document_path=sys.argv[1])
    else:
        req = ExtractionRequest(document_path="sample_invoice.pdf")

    result = extract_invoice_fields(req)
    if result.success:
        print(result.raw_response)
    else:
        print(f"Error: {result.error}")
