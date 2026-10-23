# provider: Google Vertex AI Document AI

from google.cloud import documentai_v1beta3 as documentai
from google.cloud.documentai_v1beta3.types import Document
from document_models import NormalizedExpense, RawExpenseResponse

# Local helper import for configuration
from document_client import get_vertex_ai_project, get_vertex_ai_location

PROJECT = get_vertex_ai_project()
LOCATION = get_vertex_ai_location()
PROCESSOR_ID = "projects/{}/locations/{}/processors/{}".format(
    PROJECT, LOCATION, "invoice-processor"
)

client = documentai.DocumentProcessorServiceClient()


def load_raw_expense(file_path: str) -> RawExpenseResponse:
    with open(file_path, "rb") as image:
        document = Document.from_dict(
            {"content": image.read(), "mime_type": "application/pdf"}
        )

    raw_response = client.process_document(
        name=PROCESSOR_ID, raw_document=document
    ).raw_document
    return RawExpenseResponse(content=raw_response.content)


def normalize_expense(raw: RawExpenseResponse) -> NormalizedExpense:
    # Simplified example assumes raw content is JSON-like
    import json

    data = json.loads(raw.content)
    vendor = data.get("vendor", "")
    date = data.get("date", "")
    total = data.get("total", "")
    # items may be list of dicts with description and amount
    items = [
        {
            "description": item.get("description", ""),
            "amount": item.get("amount", ""),
        }
        for item in data.get("items", [])
    ]
    return NormalizedExpense(
        vendor=vendor,
        date=date,
        total=total,
        items=items,
    )


if __name__ == "__main__":
    import sys
    from pprint import pprint

    if len(sys.argv) < 2:
        print("Usage: python normalize_expense.py <raw_expense_file.json>\n")
        sys.exit(1)

    raw_file = sys.argv[1]
    raw_response = RawExpenseResponse.from_dict(json.load(open(raw_file)))
    normalized = normalize_expense(raw_response)
    pprint(normalized.dict())
