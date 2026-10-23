from document_models import (
    ReceiptFields,
    LineItem,
    ExtractionRequest,
    ExtractionResponse,
    receipt_to_dict,
)
from document_client import (
    load_mindee_config,
    parse_receipt_response,
    MINDEE_RECEIPT_PRODUCT,
    extract_from_file_path,
    extract_from_bytes,
)

PROVIDER = "mindee"
PRODUCT = MINDEE_RECEIPT_PRODUCT


def extract_receipt_fields(request: ExtractionRequest) -> ExtractionResponse:
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

        parsed = parse_receipt_response(mindee_response)

        items = []
        for item_data in parsed.get("items", []):
            items.append(
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

        fields = ReceiptFields(
            merchant_name=parsed.get("merchant_name", ""),
            merchant_address=parsed.get("merchant_address", ""),
            receipt_date=parsed.get("receipt_date", ""),
            receipt_time=parsed.get("receipt_time", ""),
            subtotal=parsed.get("subtotal", 0.0),
            tax=parsed.get("tax", 0.0),
            tip=parsed.get("tip", 0.0),
            total=parsed.get("total", 0.0),
            currency=parsed.get("currency", "USD"),
            payment_method=parsed.get("payment_method", ""),
            items=items,
            raw_confidence=parsed.get("raw_confidence", 0.0),
            field_confidences=parsed.get("field_confidences", {}),
        )

        return ExtractionResponse(
            success=True,
            fields=fields,
            provider=PROVIDER,
            raw_response=receipt_to_dict(fields),
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
        req = ExtractionRequest(document_path="sample_receipt.jpg")

    result = extract_receipt_fields(req)
    if result.success:
        print(result.raw_response)
    else:
        print(f"Error: {result.error}")
