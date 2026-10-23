from typing import Any, Dict
from document_client import get_openai_client, get_extraction_model
from document_models import DocumentExtractionRequest, parse_json_response

MODEL_ID = get_extraction_model("receipt")


def extract_receipt_fields(document_text: str, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    client = get_openai_client()
    request = DocumentExtractionRequest(document_type="receipt", text=document_text, metadata=metadata or {})
    prompt = (
        "Extract structured receipt fields as JSON with keys: merchant, tax, total, items. "
        "Each item should include description, quantity, price, amount. "
        "Return only valid JSON.\n\n"
        f"Document:\n{request.text}"
    )
    response = client.responses.create(
        model=MODEL_ID,
        input=prompt,
        temperature=0,
    )
    data = parse_json_response(response.output_text)
    data.setdefault("document_type", "receipt")
    return data
