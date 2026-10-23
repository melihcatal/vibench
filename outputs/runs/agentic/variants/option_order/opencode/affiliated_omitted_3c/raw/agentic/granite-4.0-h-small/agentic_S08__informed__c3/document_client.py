import os
import boto3
import json

# ---------------------------------------------------------------------------
# Provider selection – set an environment variable or change the string below
# ---------------------------------------------------------------------------
# Example for Amazon Textract AnalyzeExpense
DOCUMENT_PROVIDER = os.getenv("DOC_EXTRACT_PROVIDER", "textract")

# ---------------------------------------------------------------------------
# Helper to create a configured client based on the chosen provider
# ---------------------------------------------------------------------------


def get_document_client() -> any:
    if DOCUMENT_PROVIDER == "textract":
        # Amazon Textract (AnalyzeExpense or AnalyzeDocument)
        return boto3.client("textract")
    elif DOCUMENT_PROVIDER == "alibaba":
        # Placeholder: import Alibaba SDK client if needed
        raise NotImplementedError("Alibaba OCR client not implemented yet")
    elif DOCUMENT_PROVIDER == "azure":
        # Placeholder: Azure Document Intelligence client
        raise NotImplementedError(
            "Azure Document Intelligence client not implemented yet"
        )
    elif DOCUMENT_PROVIDER == "mindee":
        # Placeholder: Mindee SDK client
        raise NotImplementedError("Mindee client not implemented yet")
    elif DOCUMENT_PROVIDER == "documentai":
        # Placeholder: Google Document AI client
        raise NotImplementedError("Google Document AI client not implemented yet")
    else:
        raise ValueError(f"Unsupported document provider: {DOCUMENT_PROVIDER}")


# ---------------------------------------------------------------------------
# Helper to call the provider's expense extraction endpoint
# ---------------------------------------------------------------------------


def extract_expense(file_bytes: bytes) -> Dict[str, Any]:
    client = get_document_client()
    if DOCUMENT_PROVIDER == "textract":
        # Amazon Textract AnalyzeExpense (requires business license)
        response = client.analyze_expense(Document={"Bytes": file_bytes})
        return build_expense_from_textract(response)
    # Add other provider branches here as they are implemented
    raise NotImplementedError(f"Extraction not implemented for {DOCUMENT_PROVIDER}")


# ---------------------------------------------------------------------------
# Internal mapper for Textract AnalyzeExpense response
# ---------------------------------------------------------------------------


def build_expense_from_textract(response: dict) -> dict:
    expense = {}
    for block in response.get("ExpenseDocuments", [{}])[0].get("ExpenseFields", []):
        txt = block.get("Text", "")
        # Simple heuristic mapping based on known field texts
        if "VENDOR" in block.get("Type", {}).get("Text", ""):
            expense["vendor"] = txt
        elif "DATE" in block.get("Type", {}).get("Text", ""):
            expense["date"] = txt
        elif "TOTAL" in block.get("Type", {}).get("Text", ""):
            expense["total"] = txt
        elif "LINE_ITEM" in block.get("Type", {}).get("Text", ""):
            # Construct a simple line‑item entry
            expense.setdefault("line_items", []).append(
                {
                    "vendor": txt if "Vendor" in block else None,
                    "description": block.get("Text", ""),
                    "amount": block.get("AmountValue", {}).get("Text"),
                }
            )
    # Optional tax field (if present)
    # Textract does not return tax directly, so you may need a second OCR call.
    return expense
